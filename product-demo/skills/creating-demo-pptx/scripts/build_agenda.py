"""Rebuild the agenda slide, or a benefits tracker slide, as the six-part agenda table.

Usage:
    python build_agenda.py <unpacked_dir> <agenda.json> [--slide slide2.xml]
    python build_agenda.py <unpacked_dir> <agenda.json> --benefits <part> --slide slideN.xml

The agenda is always the same six parts, in this order:

    intro        Intro & Whiteboard   (orange)
    observe      Observe  / Use Case 1 (blue)
    act          Act      / Use Case 2 (purple)
    secure       Secure   / Use Case 3 (red)
    why_datadog  Why Datadog          (orange)
    next_steps   Next Steps & Close   (green)

Agenda columns:   PART | USE CASE | CUSTOMER QUESTION (or FROM MY NOTES) | WHAT DEMONSTRATES IT
Tracker columns:  PART | USE CASE | BENEFITS TO <CUSTOMER> | WHAT DEMONSTRATES IT

--benefits <part> builds the benefits tracker shown after that part of the demo: parts
up to and including <part> show their benefits, <part> itself is highlighted, and later
parts are dimmed with their benefits hidden. Row heights are computed from every part's
benefits, so all six tracker slides line up exactly when you click through them.

agenda.json shape (see references/agenda.md for the full rules):

{
  "customer": "Bitsburg Bank",
  "customer_short": "Bitsburg",          (optional, used in the BENEFITS TO header)
  "has_customer_questions": true,
  "parts": {
    "intro": {
      "items": [{"text": "We have the data...", "style": "quote"}],
      "attribution": "Head of Platform",
      "demonstrates": ["6 success criteria"],
      "benefits": ["Bitsburg's own numbers on the table", "6 success criteria agreed up front"]
    },
    "observe": {
      "use_case": "See failing bill payments before customers call",
      "items": [{"text": "Why does the call center hear...?", "style": "question"}],
      "demonstrates": ["Journey Monitoring", "RUM", "APM"]
    },
    "act": {...}, "secure": {...}, "why_datadog": {...}, "next_steps": {...}
  }
}

item.style: "quote" (verbatim customer words, wrapped in curly quotes),
            "question" (paraphrased question, italic),
            "note" (plain point from the notes, used with From My Notes).

The title placeholder text becomes "Agenda for <customer>" and the slide number
placeholder is kept. Every other shape on the slide is replaced. Row heights and
font sizes are estimated so the table fits above the footer; always confirm with
the visual check loop afterwards.
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

EMU = 914400  # per inch
SLIDE_W_IN = 13.333

PARTS = [
    # key, default label, use case number, accent text, dot, light (pill fill + halo), tint (highlighted card)
    ("intro", "Intro & Whiteboard", None, "B4621A", "F0A23B", "FCE7C8", "FFF8EE"),
    ("observe", "Observe", 1, "2F4FD8", "5B8DEF", "DCE5FC", "F4F7FE"),
    ("act", "Act", 2, "6D28D9", "8B5CF6", "E6DDFB", "F7F3FE"),
    ("secure", "Secure", 3, "B42828", "E04848", "FAE3E3", "FEF5F5"),
    ("why_datadog", "Why Datadog", None, "B4621A", "F0A23B", "FCE7C8", "FFF8EE"),
    ("next_steps", "Next Steps & Close", None, "2E7D32", "4CBB5E", "D6F0DA", "F3FBF4"),
]
PART_KEYS = [p[0] for p in PARTS]

INK = "1F1F1F"
MUTED = "5F6368"
ATTRIB = "80868B"
CARD_LINE = "E2E2EA"
TIMELINE = "C9BDEB"
# Upcoming (not yet covered) rows on a benefits tracker
DIM_TEXT = "A3A7AE"
DIM_FILL = "F1F2F5"
DIM_DOT = "D3D6DC"
DIM_LINE = "ECECF1"
HALO_D = 0.44
FONT = "Roboto"

# Layout in inches
DOT_X = 0.62
DOT_D = 0.24
CARD_X, CARD_R = 0.85, 12.95
COL_PART = (1.02, 2.18)
COL_UC = (3.22, 2.55)
COL_Q = (5.97, 4.22)
COL_DEMO = (10.35, 2.45)
# Benefit lines are short, so the tracker gives some of column 3's width to the products column.
COLS_3_4 = {"agenda": (COL_Q, COL_DEMO), "benefits": ((5.97, 3.70), (9.85, 2.95))}
HEADER_Y = 1.10
ROWS_TOP = 1.44
ROWS_BOTTOM = 6.95  # Datadog footer logo starts just below
ROW_GAP = 0.07
ROW_PAD = 0.16  # top + bottom padding inside a card
ROW_MIN = 0.62

# Base font sizes in points (scaled down together if the table does not fit)
BASE = {
    "title": 40,
    "header": 11,
    "part": 19,
    "uc_label": 10.5,
    "uc_title": 13,
    "item": 12,
    "attrib": 10,
    "demo": 12.5,
    "dash": 14,
}

# Word limits from references/writing-style.md. Over-limit text stops the build.
MAX_WORDS = {"use_case": 8, "quote": 20, "question": 15, "note": 12, "attribution": 4,
             "benefit": 8, "demonstrates": 4, "label": 3}
MAX_ITEMS, MAX_BENEFITS, MAX_DEMONSTRATES = 3, 3, 5
DASH_JOINER = re.compile(r"\S\s+[\u2014\u2013-]\s+\S")

CHAR_EM = 0.47  # average glyph width as a fraction of the point size (Roboto, mixed case)
BOLD_EM = 0.50  # same for bold display text
LINE = 1.18     # line height as a multiple of point size


def text_lines(text: str, pt: float, width_in: float) -> int:
    chars_per_line = max(1, int(width_in / (pt / 72 * CHAR_EM)))
    lines = 0
    for para in text.split("\n"):
        words, cur, n = para.split(), 0, 1
        for w in words:
            add = len(w) + (1 if cur else 0)
            if cur + add > chars_per_line and cur:
                n += 1
                cur = len(w)
            else:
                cur += add
        lines += n
    return lines


def block_h(lines: int, pt: float) -> float:
    return lines * pt * LINE / 72


def emu(inches: float) -> int:
    return int(round(inches * EMU))


# ---------------------------------------------------------------- XML builders

class Ids:
    def __init__(self, start: int = 2000):
        self.n = start

    def next(self) -> int:
        self.n += 1
        return self.n


def rpr(pt, color, bold=False, italic=False):
    attrs = f'lang="en-US" sz="{int(round(pt * 100))}" b="{1 if bold else 0}" i="{1 if italic else 0}" dirty="0"'
    return (
        f"<a:rPr {attrs}><a:solidFill><a:srgbClr val=\"{color}\"/></a:solidFill>"
        f'<a:latin typeface="{FONT}"/><a:ea typeface="{FONT}"/><a:cs typeface="{FONT}"/></a:rPr>'
    )


def para(runs, space_before_pt=0, algn="l"):
    """runs: list of (text, pt, color, bold, italic)."""
    body = "".join(
        f'<a:r>{rpr(pt, c, b, i)}<a:t xml:space="preserve">{escape(t)}</a:t></a:r>'
        for t, pt, c, b, i in runs
    )
    return (
        f'<a:p><a:pPr marL="0" indent="0" algn="{algn}"><a:lnSpc><a:spcPct val="100000"/></a:lnSpc>'
        f'<a:spcBef><a:spcPts val="{int(space_before_pt * 100)}"/></a:spcBef>'
        f"<a:spcAft><a:spcPts val=\"0\"/></a:spcAft><a:buNone/></a:pPr>{body}</a:p>"
    )


def shape(ids, name, x, y, w, h, geom="rect", fill=None, line=None, line_w_pt=0.75,
          paras=None, anchor="ctr", inset=(0, 0, 0, 0), adj=None):
    sid = ids.next()
    geom_xml = f'<a:prstGeom prst="{geom}"><a:avLst/></a:prstGeom>'
    if adj is not None:
        geom_xml = f'<a:prstGeom prst="{geom}"><a:avLst><a:gd name="adj" fmla="val {adj}"/></a:avLst></a:prstGeom>'
    fill_xml = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else "<a:noFill/>"
    line_xml = (
        f'<a:ln w="{int(line_w_pt * 12700)}"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>'
        if line else "<a:ln><a:noFill/></a:ln>"
    )
    l, t, r, b = (emu(v) for v in inset)
    txt = "".join(paras) if paras else '<a:p><a:endParaRPr lang="en-US" sz="1000" dirty="0"/></a:p>'
    tx_box = ' txBox="1"' if paras and not fill and not line else ""
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="{escape(name)} {sid}"/><p:cNvSpPr{tx_box}/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>'
        f"{geom_xml}{fill_xml}{line_xml}</p:spPr>"
        f'<p:txBody><a:bodyPr wrap="square" lIns="{l}" tIns="{t}" rIns="{r}" bIns="{b}" anchor="{anchor}" anchorCtr="0" rtlCol="0">'
        f"<a:noAutofit/></a:bodyPr><a:lstStyle/>{txt}</p:txBody></p:sp>"
    )


# ---------------------------------------------------------------- spec handling

def words(text: str) -> int:
    return sum(1 for t in text.split() if re.search(r"[A-Za-z0-9]", t))


def wording_errors(key: str, row: dict) -> list[str]:
    """Concise-wording checks; see references/writing-style.md."""
    errs = []

    def check(kind, text, limit_key=None):
        n, limit = words(text), MAX_WORDS[limit_key or kind]
        if n > limit:
            errs.append(f"part '{key}' {kind} has {n} words (max {limit}): \"{text}\"")
        if kind != "quote" and DASH_JOINER.search(text):
            errs.append(f"part '{key}' {kind} joins clauses with a dash; use a comma, colon or new line: \"{text}\"")

    if row.get("label"):
        check("label", row["label"])
    if row.get("use_case"):
        check("use_case", row["use_case"])
    if row.get("attribution"):
        check("attribution", row["attribution"])
    for item in row.get("items", []):
        check(item.get("style", "note"), item.get("text", ""))
    for b in row.get("benefits", []):
        check("benefit", b)
    for d in row.get("demonstrates", []):
        check("demonstrates", d)
    if len(row.get("items", [])) > MAX_ITEMS:
        errs.append(f"part '{key}' has {len(row['items'])} items (max {MAX_ITEMS}); keep the strongest")
    if len(row.get("benefits", [])) > MAX_BENEFITS:
        errs.append(f"part '{key}' has {len(row['benefits'])} benefits (max {MAX_BENEFITS}); keep the strongest")
    if len(row.get("demonstrates", [])) > MAX_DEMONSTRATES:
        errs.append(f"part '{key}' lists {len(row['demonstrates'])} demonstrates entries (max {MAX_DEMONSTRATES})")
    return errs


def load_spec(path: Path, need_benefits: bool) -> dict:
    spec = json.loads(path.read_text())
    errors = []
    if not spec.get("customer"):
        errors.append("'customer' is required (the real prospect/customer name)")
    parts = spec.get("parts", {})
    unknown = set(parts) - {p[0] for p in PARTS}
    if unknown:
        errors.append(f"unknown part keys {sorted(unknown)}; allowed: {[p[0] for p in PARTS]}")
    for key, _label, uc, *_ in PARTS:
        row = parts.get(key)
        if row is None:
            errors.append(f"part '{key}' is missing; the agenda always has all six parts")
            continue
        if uc and not row.get("use_case"):
            errors.append(f"part '{key}' needs a 'use_case' title (Use Case {uc})")
        if not row.get("items"):
            errors.append(f"part '{key}' needs at least one item")
        if not row.get("demonstrates"):
            errors.append(f"part '{key}' needs at least one 'demonstrates' entry")
        for item in row.get("items", []):
            if item.get("style", "note") not in ("quote", "question", "note"):
                errors.append(f"part '{key}': item style must be quote, question or note")
        if need_benefits and not row.get("benefits"):
            errors.append(f"part '{key}' needs at least one 'benefits' line for the benefits tracker")
        errors.extend(wording_errors(key, row))
    if errors:
        sys.exit("agenda spec errors:\n  - " + "\n  - ".join(errors))
    return spec


def item_text(item) -> str:
    t = item["text"].strip()
    if item.get("style") == "quote":
        t = t.strip("\"“”")
        t = f"“{t}”"
    return t


def column3(row, mode):
    """Third-column paragraphs as (text, italic) pairs, plus an optional attribution line."""
    if mode == "benefits":
        return [(b.strip(), False) for b in row["benefits"]], None
    return [(item_text(i), i.get("style") == "question") for i in row["items"]], row.get("attribution")


def scaled(s):
    """Font sizes at scale s. Part labels and dashes shrink less: they are rarely the constraint."""
    f = {k: v * s for k, v in BASE.items()}
    f["part"] = BASE["part"] * max(s, 0.85)
    f["dash"] = BASE["dash"] * max(s, 0.85)
    return f


def fit_part_labels(spec, f):
    """Keep every part label on one line, at one shared size, so the left column reads evenly."""
    labels = [spec["parts"][k].get("label", label) for k, label, *_ in PARTS]
    one_line = min(COL_PART[1] * 72 / (len(t) * BOLD_EM) for t in labels)
    f["part"] = max(14, min(f["part"], one_line))
    return f


def measure(spec, s, mode):
    """Return row heights in inches at font scale s."""
    f = fit_part_labels(spec, scaled(s))
    heights = []
    for key, label, uc, *_ in PARTS:
        row = spec["parts"][key]
        label = row.get("label", label)
        part_h = block_h(text_lines(label, f["part"], COL_PART[1]), f["part"])
        if uc:
            pill_w = COL_UC[1] - 0.35
            uc_lines = text_lines(row["use_case"], f["uc_title"] * BOLD_EM / CHAR_EM, pill_w)
            uc_h = (block_h(1, f["uc_label"]) + block_h(uc_lines, f["uc_title"]) + 0.22)
        else:
            uc_h = block_h(1, f["dash"])
        col_q, col_demo = COLS_3_4[mode]
        q_h = 0.0
        lines, attribution = column3(row, mode)
        for i, (text, _italic) in enumerate(lines):
            q_h += block_h(text_lines(text, f["item"], col_q[1]), f["item"])
            if i:
                q_h += 4 * s / 72
        if attribution:
            q_h += block_h(1, f["attrib"]) + 3 / 72
        demo_h = block_h(text_lines(" · ".join(row["demonstrates"]), f["demo"], col_demo[1]), f["demo"])
        heights.append(max(ROW_MIN, ROW_PAD + max(part_h, uc_h, q_h, demo_h)))
    return heights


def fit(spec, mode):
    avail = ROWS_BOTTOM - ROWS_TOP - ROW_GAP * (len(PARTS) - 1)
    s = 1.0
    while True:
        heights = measure(spec, s, mode)
        if sum(heights) <= avail or s <= 0.72:
            break
        s = round(s - 0.04, 2)
    total = sum(heights)
    if total > avail:
        print(f"WARNING: agenda content is too long even at {int(s * 100)}% font size "
              f"({total:.2f}in for {avail:.2f}in). Shorten the items.", file=sys.stderr)
    else:
        # Spread spare height evenly so the table fills the slide like the reference design.
        extra = min((avail - total) / len(heights), 0.30)
        heights = [h + extra for h in heights]
    return s, heights


# ---------------------------------------------------------------- slide assembly

def column3_header(spec, mode):
    if mode == "benefits":
        return f"BENEFITS TO {spec.get('customer_short') or spec['customer']}".upper()
    return "CUSTOMER QUESTION" if spec.get("has_customer_questions") else "FROM MY NOTES"


def build_shapes(spec, s, heights, mode="agenda", current=None):
    f = fit_part_labels(spec, scaled(s))
    ids = Ids()
    out = []
    header_q = column3_header(spec, mode)
    col_q, col_demo = COLS_3_4[mode]
    cur = PART_KEYS.index(current) if current else None

    # Column headers
    for (x, w), text in ((COL_PART, "PART"), (COL_UC, "USE CASE"), (col_q, header_q),
                         (col_demo, "WHAT DEMONSTRATES IT")):
        out.append(shape(ids, "Agenda Header", x, HEADER_Y, w, 0.30, anchor="b",
                         paras=[para([(text, f["header"], MUTED, True, False)])]))

    # Row geometry
    tops, y = [], ROWS_TOP
    for h in heights:
        tops.append(y)
        y += h + ROW_GAP

    # Timeline behind the dots
    first_c = tops[0] + heights[0] / 2
    last_c = tops[-1] + heights[-1] / 2
    out.append(shape(ids, "Agenda Timeline", DOT_X - 0.015, first_c, 0.03, last_c - first_c,
                     fill=TIMELINE))

    for i, ((key, label, uc, accent, dot, light, tint), top, h) in enumerate(zip(PARTS, tops, heights)):
        row = spec["parts"][key]
        label = row.get("label", label)
        cy = top + h / 2
        state = "normal" if cur is None else ("current" if i == cur else ("done" if i < cur else "upcoming"))
        upcoming = state == "upcoming"

        if state == "current":
            out.append(shape(ids, "Agenda Card", CARD_X, top, CARD_R - CARD_X, h, geom="roundRect",
                             fill=tint, line=dot, line_w_pt=1.75, adj=12000))
            out.append(shape(ids, "Agenda Halo", DOT_X - HALO_D / 2, cy - HALO_D / 2, HALO_D, HALO_D,
                             geom="ellipse", fill=light))
        else:
            out.append(shape(ids, "Agenda Card", CARD_X, top, CARD_R - CARD_X, h, geom="roundRect",
                             fill="FFFFFF", line=DIM_LINE if upcoming else CARD_LINE, adj=12000))
        out.append(shape(ids, "Agenda Dot", DOT_X - DOT_D / 2, cy - DOT_D / 2, DOT_D, DOT_D,
                         geom="ellipse", fill=DIM_DOT if upcoming else dot, line="FFFFFF", line_w_pt=2))

        # Part
        out.append(shape(ids, "Agenda Part", COL_PART[0], top, COL_PART[1], h,
                         paras=[para([(label, f["part"], DIM_TEXT if upcoming else accent, True, False)])]))

        # Use case pill or dash
        if uc:
            out.append(shape(ids, "Agenda Use Case", COL_UC[0], top + 0.07, COL_UC[1], h - 0.14,
                             geom="roundRect", fill=DIM_FILL if upcoming else light, adj=14000,
                             inset=(0.15, 0.06, 0.12, 0.06),
                             paras=[para([(f"Use Case {uc}", f["uc_label"], DIM_TEXT if upcoming else accent, True, False)]),
                                    para([(row["use_case"], f["uc_title"], DIM_TEXT if upcoming else INK, True, False)], 1)]))
        else:
            out.append(shape(ids, "Agenda Use Case", COL_UC[0] + 0.15, top, COL_UC[1] - 0.15, h,
                             paras=[para([("—", f["dash"], DIM_TEXT if upcoming else MUTED, False, False)])]))

        # Upcoming rows on a tracker keep their benefits and products hidden until covered.
        if upcoming:
            continue

        # Customer question / from my notes / benefits
        lines, attribution = column3(row, mode)
        q_paras = [para([(text, f["item"], INK, False, italic)], 4 * s if j else 0)
                   for j, (text, italic) in enumerate(lines)]
        if attribution:
            q_paras.append(para([(attribution, f["attrib"], ATTRIB, False, False)], 3))
        out.append(shape(ids, "Agenda Notes", col_q[0], top, col_q[1], h, paras=q_paras))

        # What demonstrates it
        out.append(shape(ids, "Agenda Demonstrates", col_demo[0], top, col_demo[1], h,
                         paras=[para([(" · ".join(row["demonstrates"]), f["demo"], accent, True, False)])]))
    return "".join(out)


def set_title(title_sp: str, text: str) -> str:
    pt = BASE["title"]
    width = 11.8
    while pt > 30 and len(text) * pt / 72 * CHAR_EM > width:
        pt -= 2
    title_sp = re.sub(r'<a:ext cx="\d+" cy="(\d+)"/>', lambda m: f'<a:ext cx="{emu(width)}" cy="{m.group(1)}"/>',
                      title_sp, count=1)
    # Keep the first paragraph's formatting, replace its runs with one run.
    run = (f'<a:r>{rpr(pt, "000000", bold=True)}<a:t>{escape(text)}</a:t></a:r>')
    body = re.search(r"<p:txBody>.*</p:txBody>", title_sp, re.S).group(0)
    first_p = re.search(r"<a:p>.*?</a:p>", body, re.S).group(0)
    ppr = re.search(r"<a:pPr[^>]*/>|<a:pPr.*?</a:pPr>", first_p, re.S)
    new_p = f"<a:p>{ppr.group(0) if ppr else ''}{run}</a:p>"
    new_body = re.sub(r"<a:p>.*</a:p>", lambda _: new_p, body, count=1, flags=re.S)
    return title_sp.replace(body, new_body)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("unpacked_dir", type=Path)
    ap.add_argument("spec", type=Path)
    ap.add_argument("--slide", default="slide2.xml", help="slide file to rebuild (default: slide2.xml)")
    ap.add_argument("--benefits", choices=PART_KEYS, metavar="PART",
                    help=f"build the benefits tracker shown after PART ({', '.join(PART_KEYS)})")
    args = ap.parse_args()
    mode = "benefits" if args.benefits else "agenda"
    if args.benefits and args.slide == "slide2.xml":
        sys.exit("--benefits needs --slide pointing at a duplicated slide, not the agenda (slide2.xml)")

    spec = load_spec(args.spec, need_benefits=bool(args.benefits))
    slide_path = args.unpacked_dir / "ppt" / "slides" / args.slide
    if not slide_path.exists():
        sys.exit(f"{slide_path} not found")
    xml = slide_path.read_text(encoding="utf-8")

    tree = re.search(r"<p:spTree>.*</p:spTree>", xml, re.S)
    if not tree:
        sys.exit("no <p:spTree> in slide")
    head = re.search(r"<p:spTree>.*?</p:grpSpPr>", tree.group(0), re.S).group(0)
    leaf_sps = re.findall(r"<p:sp>(?:(?!<p:sp>).)*?</p:sp>", tree.group(0), re.S)
    title = next((sp for sp in leaf_sps if re.search(r'<p:ph type="(title|ctrTitle)"', sp)), None)
    sldnum = next((sp for sp in leaf_sps if '<p:ph type="sldNum"' in sp), "")
    if title is None:
        sys.exit("agenda slide has no title placeholder; duplicate the template's agenda slide (slide2.xml)")

    s, heights = fit(spec, mode)
    new_tree = (head + set_title(title, f"Agenda for {spec['customer']}") + sldnum
                + build_shapes(spec, s, heights, mode, args.benefits) + "</p:spTree>")
    xml = xml[:tree.start()] + new_tree + xml[tree.end():]
    slide_path.write_text(xml, encoding="utf-8")

    what = f"Benefits tracker (after {args.benefits})" if args.benefits else "Agenda"
    print(f"{what} written to {slide_path} (font scale {int(s * 100)}%, "
          f"third column: {column3_header(spec, mode).title()}, "
          f"rows end at {ROWS_TOP + sum(heights) + ROW_GAP * 5:.2f}in)")


if __name__ == "__main__":
    main()
