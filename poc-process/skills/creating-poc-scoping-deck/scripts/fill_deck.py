#!/usr/bin/env python3
"""List and fill the placeholder tokens in an unpacked PoC scoping deck.

Usage:
    python3 fill_deck.py --list  <unpacked_dir> [--pretty]
    python3 fill_deck.py --apply <unpacked_dir> --map fill.json [--report]

Examples:
    python3 fill_deck.py --list unpacked/ --pretty
    python3 fill_deck.py --apply unpacked/ --map fill.json --report

Why this script exists: PowerPoint splits one visible string across several <a:r> runs
whenever formatting, spell-check state, or editing history changes mid-word. So
`[Prospect / Customer Name]` is often stored as `[Prospect`, ` / Customer`, ` Name]` in
three separate <a:t> elements. A plain search-and-replace misses those and fails
silently, leaving brackets in a deck that looks finished. This script matches across
the whole paragraph, so a token is either replaced or reported as a miss.

Replacement strategy, in order of preference:
  1. If every occurrence sits inside a single run, replace run by run. Run-level
     formatting (bold, colour, size) is preserved exactly.
  2. Otherwise the token spans runs, so the paragraph's whole text is rebuilt into its
     first run and the remaining runs are emptied. The paragraph inherits the first
     run's formatting, which is the right call for the bracketed placeholders in this
     template because they are uniformly formatted.

Map format (fill.json) — a JSON object of token to replacement:

    {
      "[Prospect / Customer Name]": "Acme Corp",
      "Jek Bao Choo": "Sam Rivera",
      "8:[email]": ["ae@datadoghq.com", "se@datadoghq.com", "champion@acme.com"],
      "6:…": ["Tuesdays 10:00 SGT", "Thursdays 16:00 SGT", "Ad hoc"]
    }

A string value replaces every occurrence. A list value replaces successive occurrences
in document order — use it for repeated tokens like the `…` cadence blanks and the
duplicated `[12]` on the MTTD slide. Extra occurrences beyond the end of the list are
left untouched and reported as remaining.

Repeated tokens need scoping, and there are two ways to do it:

  "8:[email]"                      restrict to slide 8
  "[Champion Name] >> [email]"     restrict to the shape that also contains the anchor

Prefer the anchor form. Document order is not visual order — on slide 8 the prospect's
contact panel is stored before Datadog's even though it renders on the right, so an
ordered list scoped only by slide silently puts the AE's address in the champion's
slot. Anchoring to a unique neighbouring token ("the email in the block that also has
[Champion Name]") is order-independent and reads the way you actually think about it.

The two forms combine: "8:[Champion Name] >> [email]". Run `--list` first — it groups
tokens by shape, so you can see which tokens share a block and pick an anchor.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree

A_NS = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P_NS = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
R_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PKG_NS = "{http://schemas.openxmlformats.org/package/2006/relationships}"

# A bracketed fill-in slot: [Date], [Success criteria 1], ~[19,000]. Kept deliberately
# tight (no nesting, no newlines, bounded length) so real prose in square brackets is
# not mistaken for a placeholder.
TOKEN_RE = re.compile(r"\[[^\[\]\n]{1,80}\]")

# The blank-line marker the template uses on the cadence slides.
BLANK = "…"

# Two values are baked into the template as literal text rather than brackets, so they
# look filled-in when they are not. Surfacing them here stops a stale name reaching a
# prospect. See references/slide-map.md.
KNOWN_LITERALS = ("Jek Bao Choo", "VP of Engineering")

PARA_RE = re.compile(r"<a:p>.*?</a:p>", re.DOTALL)
TEXT_RE = re.compile(r"<a:t(\s[^>]*)?>(.*?)</a:t>|<a:t\s*/>", re.DOTALL)
# <p:sp> never nests inside another <p:sp>, so a non-greedy match is safe here.
SHAPE_RE = re.compile(r"<p:sp>.*?</p:sp>", re.DOTALL)

ANCHOR_SEP = " >> "


def unescape(text):
    """XML text to plain text, including the numeric refs unpack.py introduces."""
    text = re.sub(r"&#x([0-9A-Fa-f]+);", lambda m: chr(int(m.group(1), 16)), text)
    text = re.sub(r"&#(\d+);", lambda m: chr(int(m.group(1))), text)
    for entity, char in (("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'),
                         ("&apos;", "'"), ("&amp;", "&")):
        text = text.replace(entity, char)
    return text


def escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def slide_order(unpacked):
    """Slide files in presentation order. Filename number != display position."""
    pres = unpacked / "ppt" / "presentation.xml"
    rels = unpacked / "ppt" / "_rels" / "presentation.xml.rels"
    if not pres.is_file() or not rels.is_file():
        raise SystemExit(f"{unpacked} does not look like an unpacked .pptx.")

    targets = {
        rel.get("Id"): rel.get("Target")
        for rel in ElementTree.parse(rels).getroot().iter(f"{PKG_NS}Relationship")
    }
    ordered = []
    root = ElementTree.parse(pres).getroot()
    for sld in root.iter(f"{P_NS}sldId"):
        target = targets.get(sld.get(f"{R_NS}id"), "")
        name = Path(target).name
        path = unpacked / "ppt" / "slides" / name
        if path.is_file():
            ordered.append(path)
    return ordered


def list_tokens(unpacked):
    """Read-only inventory of every placeholder, by slide position and shape name."""
    slides = []
    counts = {}
    blanks_total = 0
    literals_total = {}

    for position, path in enumerate(slide_order(unpacked), 1):
        root = ElementTree.parse(path).getroot()
        shapes = []
        blanks = 0
        for shape in root.iter(f"{P_NS}sp"):
            name_el = shape.find(f".//{P_NS}cNvPr")
            shape_name = name_el.get("name", "") if name_el is not None else ""
            lines, tokens = [], []
            for para in shape.iter(f"{A_NS}p"):
                text = "".join(t.text or "" for t in para.iter(f"{A_NS}t"))
                if text.strip():
                    lines.append(text.strip())
                for token in TOKEN_RE.findall(text):
                    tokens.append(token)
                    counts[token] = counts.get(token, 0) + 1
                blanks += text.count(BLANK)
            if tokens or BLANK in " ".join(lines):
                shapes.append({
                    "shape": shape_name,
                    # Grouping tokens with their neighbouring text is the point: it
                    # shows which unique token can anchor an ambiguous one.
                    "text": " / ".join(lines)[:300],
                    "tokens": tokens,
                    "blanks": " ".join(lines).count(BLANK),
                })

        literals = []
        raw = unescape(path.read_text(encoding="utf-8"))
        for literal in KNOWN_LITERALS:
            if literal in raw:
                literals.append(literal)
                literals_total[literal] = literals_total.get(literal, 0) + 1

        blanks_total += blanks
        slides.append({
            "position": position,
            "file": path.name,
            "shapes": shapes,
            "blanks": blanks,
            "literals": literals,
        })

    return {
        "slides": slides,
        "summary": {
            "slide_count": len(slides),
            "token_occurrences": sum(counts.values()),
            "unique_tokens": dict(sorted(counts.items())),
            "blank_markers": blanks_total,
            "literals": literals_total,
        },
    }


def fill_paragraph(block, token, take):
    """Replace occurrences of `token` in one <a:p> block. Returns (block, n_replaced).

    `take()` yields the next replacement, or None when the caller has run out.
    """
    spans = list(TEXT_RE.finditer(block))
    if not spans:
        return block, 0

    runs = [unescape(m.group(2)) if m.group(0) != "<a:t/>" and m.group(2) is not None
            else "" for m in spans]
    joined = "".join(runs)
    if token not in joined:
        return block, 0

    per_run = sum(r.count(token) for r in runs)
    total = joined.count(token)

    if per_run == total:
        # Every occurrence is self-contained; edit runs in place and keep formatting.
        replaced = 0
        new_runs = []
        for run in runs:
            out = run
            while token in out:
                value = take()
                if value is None:
                    break
                out = out.replace(token, value, 1)
                replaced += 1
            new_runs.append(out)
        if not replaced:
            return block, 0
        return rewrite(block, spans, new_runs), replaced

    # The token straddles runs. Rebuild the paragraph text into the first run.
    replaced = 0
    out = joined
    while token in out:
        value = take()
        if value is None:
            break
        out = out.replace(token, value, 1)
        replaced += 1
    if not replaced:
        return block, 0
    new_runs = [out] + [""] * (len(runs) - 1)
    return rewrite(block, spans, new_runs), replaced


def rewrite(block, spans, new_runs):
    """Write new_runs back into the <a:t> positions recorded in spans."""
    pieces = []
    cursor = 0
    for match, text in zip(spans, new_runs):
        pieces.append(block[cursor:match.start()])
        attrs = match.group(1) or ""
        if text != text.strip():
            # Leading or trailing whitespace is dropped by consumers unless declared.
            if "xml:space" not in attrs:
                attrs += ' xml:space="preserve"'
        pieces.append(f"<a:t{attrs}>{escape(text)}</a:t>")
        cursor = match.end()
    pieces.append(block[cursor:])
    return "".join(pieces)


SCOPED_KEY_RE = re.compile(r"^(\d+):(.+)$", re.DOTALL)


def search_regions(xml, anchor):
    """Byte ranges of the slide to search, in document order.

    With no anchor that is the whole slide. With one, it is only those <p:sp> shapes
    whose visible text contains the anchor — which is how an ambiguous token gets
    pinned to the right block.
    """
    if not anchor:
        return [(0, len(xml))]
    regions = []
    for match in SHAPE_RE.finditer(xml):
        text = "".join(
            unescape(m.group(2) or "") for m in TEXT_RE.finditer(match.group(0))
        )
        if anchor in text:
            regions.append((match.start(), match.end()))
    return regions


def apply_map(unpacked, mapping):
    """Apply the token map across every slide in presentation order."""
    slides = slide_order(unpacked)
    positions = {path: i for i, path in enumerate(slides, 1)}
    contents = {path: path.read_text(encoding="utf-8") for path in slides}
    hits = {}

    # Anchored keys run first. An anchor is matched against the slide as it stands, so
    # if an unanchored key had already replaced "[Champion Name]" with a real name the
    # anchor would no longer resolve and the fill would silently do nothing.
    ordered_keys = sorted(mapping, key=lambda k: ANCHOR_SEP not in k)

    for key in ordered_keys:
        value = mapping[key]
        scoped = SCOPED_KEY_RE.match(key)
        only_slide = int(scoped.group(1)) if scoped else None
        token = scoped.group(2) if scoped else key
        anchor = None
        if ANCHOR_SEP in token:
            anchor, token = token.split(ANCHOR_SEP, 1)
            anchor, token = anchor.strip(), token.strip()
        if only_slide is not None and only_slide not in positions.values():
            raise SystemExit(
                f"Key {key!r} targets slide {only_slide}, but the deck has "
                f"{len(slides)} slides."
            )

        if isinstance(value, str):
            values, unlimited = [value], True
        elif isinstance(value, list) and all(isinstance(v, str) for v in value):
            values, unlimited = list(value), False
        else:
            raise SystemExit(
                f"Value for {key!r} must be a string or a list of strings."
            )

        state = {"i": 0}

        def take():
            if unlimited:
                return values[0]
            if state["i"] >= len(values):
                return None
            state["i"] += 1
            return values[state["i"] - 1]

        replaced = 0
        for path in slides:
            if only_slide is not None and positions[path] != only_slide:
                continue
            xml = contents[path]
            # Walk regions forward so `take()` consumes values in document order, but
            # collect the edits and splice them in backwards — otherwise the first
            # rewrite shifts every later offset.
            edits = []
            for start, end in search_regions(xml, anchor):
                sub = xml[start:end]
                out = []
                cursor = 0
                for match in PARA_RE.finditer(sub):
                    new_block, n = fill_paragraph(match.group(0), token, take)
                    if n:
                        out.append(sub[cursor:match.start()])
                        out.append(new_block)
                        cursor = match.end()
                        replaced += n
                if cursor:
                    out.append(sub[cursor:])
                    edits.append((start, end, "".join(out)))
            for start, end, new_sub in reversed(edits):
                xml = xml[:start] + new_sub + xml[end:]
            contents[path] = xml
        hits[key] = replaced

    for path, xml in contents.items():
        path.write_text(xml, encoding="utf-8")
    return hits


def main():
    parser = argparse.ArgumentParser(
        description="List and fill placeholder tokens in an unpacked PoC scoping deck."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--list", metavar="UNPACKED_DIR",
                      help="report every placeholder as JSON on stdout")
    mode.add_argument("--apply", metavar="UNPACKED_DIR",
                      help="apply a token map to the slides in place")
    parser.add_argument("--map", metavar="FILL_JSON",
                        help="JSON object of token to replacement (required with --apply)")
    parser.add_argument("--pretty", action="store_true",
                        help="indent the --list JSON")
    parser.add_argument("--report", action="store_true",
                        help="after --apply, print hit counts and what remains")
    args = parser.parse_args()

    if args.list:
        report = list_tokens(Path(args.list).expanduser())
        print(json.dumps(report, indent=2 if args.pretty else None, ensure_ascii=False))
        return

    unpacked = Path(args.apply).expanduser()
    if not args.map:
        raise SystemExit("--apply requires --map.")
    mapping = json.loads(Path(args.map).expanduser().read_text(encoding="utf-8"))
    if not isinstance(mapping, dict):
        raise SystemExit("The map file must contain a JSON object.")

    hits = apply_map(unpacked, mapping)

    for token, count in hits.items():
        print(f"{count:4d}  {token}")
    missed = [t for t, c in hits.items() if c == 0]
    if missed:
        print(f"\nNo match for {len(missed)} token(s): {', '.join(missed)}",
              file=sys.stderr)

    if args.report:
        after = list_tokens(unpacked)["summary"]
        print(
            f"\nRemaining: {after['token_occurrences']} bracketed token(s), "
            f"{after['blank_markers']} blank marker(s), "
            f"{sum(after['literals'].values())} known literal(s)."
        )
        if after["unique_tokens"]:
            print("Still unfilled: " + ", ".join(after["unique_tokens"]))
        print("Every one of these must appear in open-questions.md.")

    if missed:
        sys.exit(1)


if __name__ == "__main__":
    main()
