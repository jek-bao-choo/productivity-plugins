"""Check a finished deck for wordy text, per references/writing-style.md.

Usage: python check_wording.py output.pptx

Flags, per slide (in presentation order):
  - a title over 8 words
  - a body line (paragraph) over 12 words
  - more than 60 words on the slide, excluding the title
  - filler words (leverage, robust, seamless, ...)
  - clauses joined with " — " or " - "
  - leftover template placeholders ([Name of ...], lorem ipsum)

Agenda and benefits tracker slides built by build_agenda.py are skipped; that script
enforces its own limits. Exits 1 when anything is flagged, 0 when the deck is clean.
"""

import html
import re
import sys
import zipfile
from pathlib import PurePosixPath

TITLE_MAX = 8
LINE_MAX = 12
SLIDE_MAX = 60

FILLER = [
    "in order to", "leverage", "leverages", "leveraging", "utilize", "utilizes", "utilizing",
    "seamless", "seamlessly", "robust", "comprehensive", "holistic", "cutting-edge",
    "best-in-class", "world-class", "state-of-the-art", "empower", "empowers", "unlock",
    "unlocks", "game-changing", "very", "really", "basically", "actually",
]
FILLER_RE = re.compile(r"(?<![\w-])(" + "|".join(re.escape(f) for f in FILLER) + r")(?![\w-])", re.I)
DASH_JOINER_RE = re.compile(r"\S\s+[—–-]\s+\S")
PLACEHOLDER_RE = re.compile(r"\[[^\]]{3,}\]|lorem|ipsum", re.I)
SKIP_PH = {"sldNum", "ftr", "dt"}


def words(text: str) -> int:
    return sum(1 for t in text.split() if re.search(r"[A-Za-z0-9]", t))


def slide_order(z: zipfile.ZipFile) -> list[str]:
    pres = z.read("ppt/presentation.xml").decode("utf-8")
    rels = z.read("ppt/_rels/presentation.xml.rels").decode("utf-8")
    targets = {m.group(1): m.group(2) for m in
               re.finditer(r'Id="(rId\d+)"[^>]*?Target="([^"]+)"', rels)}
    targets.update({m.group(2): m.group(1) for m in
                    re.finditer(r'Target="([^"]+)"[^>]*?Id="(rId\d+)"', rels)})
    order = []
    for rid in re.findall(r'<p:sldId [^>]*r:id="(rId\d+)"', pres):
        order.append(str(PurePosixPath("ppt") / targets[rid]))
    return order


def shapes(xml: str):
    """Yield (placeholder type or None, [paragraph text, ...]) for each text shape."""
    for sp in re.findall(r"<p:sp>(?:(?!<p:sp>).)*?</p:sp>", xml, re.S):
        ph = re.search(r'<p:ph[^>]*type="(\w+)"', sp)
        paras = []
        for p in re.findall(r"<a:p>.*?</a:p>|<a:p .*?</a:p>", sp, re.S):
            text = "".join(re.findall(r"<a:t[^>]*>(.*?)</a:t>", p, re.S))
            text = html.unescape(text).strip()
            if text:
                paras.append(text)
        if paras:
            yield (ph.group(1) if ph else None), paras
    # Tables: one cell paragraph at a time
    for tc in re.findall(r"<a:tc>.*?</a:tc>", xml, re.S):
        for p in re.findall(r"<a:p>.*?</a:p>", tc, re.S):
            text = html.unescape("".join(re.findall(r"<a:t[^>]*>(.*?)</a:t>", p, re.S))).strip()
            if text:
                yield "cell", [text]


def check(path: str) -> int:
    issues = []
    with zipfile.ZipFile(path) as z:
        for n, name in enumerate(slide_order(z), 1):
            xml = z.read(name).decode("utf-8")
            if 'name="Agenda Card' in xml:
                continue
            total = 0
            for ph, paras in shapes(xml):
                if ph in SKIP_PH:
                    continue
                is_title = ph in ("title", "ctrTitle")
                for text in paras:
                    w = words(text)
                    short = text if len(text) <= 70 else text[:67] + "..."
                    if is_title and w > TITLE_MAX:
                        issues.append((n, f"title has {w} words (max {TITLE_MAX})", short))
                    if not is_title:
                        total += w
                        if w > LINE_MAX:
                            issues.append((n, f"line has {w} words (max {LINE_MAX})", short))
                    for m in FILLER_RE.finditer(text):
                        issues.append((n, f'filler word "{m.group(1)}"', short))
                    if DASH_JOINER_RE.search(text):
                        issues.append((n, "dash joins two clauses; use a comma, colon or new line", short))
                    if PLACEHOLDER_RE.search(text):
                        issues.append((n, "leftover template placeholder", short))
            if total > SLIDE_MAX:
                issues.append((n, f"slide has {total} words (max {SLIDE_MAX}); cut the weakest points", ""))

    if not issues:
        print("Wording check passed: every slide is within the limits.")
        return 0
    print(f"Wording check: {len(issues)} issue(s)\n")
    print("| Slide | Issue | Text |\n|---|---|---|")
    for n, issue, text in issues:
        print(f"| S{n} | {issue} | {text.replace('|', '/')} |")
    return 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(check(sys.argv[1]))
