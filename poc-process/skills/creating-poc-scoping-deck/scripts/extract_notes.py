#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pypdf"]
# ///
"""Extract meeting notes from mixed file formats into one markdown stream.

Reads each input file and writes markdown to stdout, prefixed by a `## <filename>`
header, so a whole pile of discovery artefacts can be read as a single document.

Usage:
    python3 extract_notes.py <file> [<file> ...]

Examples:
    python3 extract_notes.py notes.md transcript.docx costs.xlsx
    uv run extract_notes.py discovery.pdf          # uv installs pypdf automatically

Supported: .md .txt .docx .xlsx .pdf .gdoc

Only .pdf needs a third-party package (pypdf); everything else is stdlib. The PEP 723
block above lets `uv run` provide pypdf without touching the system environment. Under
plain `python3`, non-PDF inputs still work and a PDF input reports what to install.

A .gdoc file on macOS is a JSON stub holding a Google Docs URL, not the document text.
There is nothing to extract locally, so this prints a `GDOC_URL: <url>` marker line for
the caller to fetch, rather than pretending the file was empty.
"""

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
X_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
PKG_NS = "{http://schemas.openxmlformats.org/package/2006/relationships}"

SUPPORTED = (".md", ".txt", ".docx", ".xlsx", ".pdf", ".gdoc")


def read_text(path):
    return path.read_text(encoding="utf-8", errors="replace").strip()


def read_docx(path):
    """One markdown line per w:p, keeping heading levels and list indentation."""
    with zipfile.ZipFile(path) as zf:
        xml = zf.read("word/document.xml")
    root = ElementTree.fromstring(xml)
    lines = []
    for para in root.iter(f"{W_NS}p"):
        text = "".join(t.text or "" for t in para.iter(f"{W_NS}t")).strip()
        if not text:
            continue
        style = para.find(f"{W_NS}pPr/{W_NS}pStyle")
        style_id = style.get(f"{W_NS}val", "") if style is not None else ""
        heading = re.match(r"Heading(\d)", style_id)
        if heading:
            lines.append(f"{'#' * min(int(heading.group(1)) + 2, 6)} {text}")
        elif (para.find(f"{W_NS}pPr/{W_NS}numPr") is not None
              or style_id.startswith(("List", "ListParagraph"))):
            # Bullets come through either as real numbering or as a List* style,
            # depending on which editor produced the file.
            lines.append(f"- {text}")
        else:
            lines.append(text)
    return "\n\n".join(lines)


def read_xlsx(path):
    """Every sheet as a markdown table. Shared strings resolved; formulas give values."""
    with zipfile.ZipFile(path) as zf:
        shared = []
        if "xl/sharedStrings.xml" in zf.namelist():
            sst = ElementTree.fromstring(zf.read("xl/sharedStrings.xml"))
            for si in sst.iter(f"{X_NS}si"):
                shared.append("".join(t.text or "" for t in si.iter(f"{X_NS}t")))

        # Sheet name -> target path, via the workbook's relationships.
        rels = {
            rel.get("Id"): rel.get("Target")
            for rel in ElementTree.fromstring(
                zf.read("xl/_rels/workbook.xml.rels")
            ).iter(f"{PKG_NS}Relationship")
        }
        sheets = []
        for sheet in ElementTree.fromstring(zf.read("xl/workbook.xml")).iter(
            f"{X_NS}sheet"
        ):
            rid = sheet.get(
                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
            )
            target = rels.get(rid, "")
            # Targets come either absolute ("/xl/worksheets/sheet1.xml") or relative
            # to xl/ ("worksheets/sheet1.xml"), depending on the writer.
            part = target.lstrip("/") if target.startswith("/") else "xl/" + target
            sheets.append((sheet.get("name", "Sheet"), part))

        out = []
        for name, target in sheets:
            if target not in zf.namelist():
                continue
            rows = []
            for row in ElementTree.fromstring(zf.read(target)).iter(f"{X_NS}row"):
                cells = []
                for cell in row.iter(f"{X_NS}c"):
                    value = cell.find(f"{X_NS}v")
                    inline = cell.find(f"{X_NS}is")
                    if cell.get("t") == "s" and value is not None:
                        cells.append(shared[int(value.text)])
                    elif inline is not None:
                        cells.append("".join(t.text or "" for t in inline.iter(f"{X_NS}t")))
                    elif value is not None:
                        cells.append(value.text or "")
                    else:
                        cells.append("")
                if any(c.strip() for c in cells):
                    rows.append(cells)
            if not rows:
                continue
            width = max(len(r) for r in rows)
            rows = [r + [""] * (width - len(r)) for r in rows]
            table = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * width]
            table += ["| " + " | ".join(r) + " |" for r in rows[1:]]
            out.append(f"### Sheet: {name}\n\n" + "\n".join(table))
        return "\n\n".join(out)


def read_pdf(path):
    try:
        from pypdf import PdfReader
    except ImportError:
        raise SystemExit(
            f"Reading {path.name} needs pypdf. Either run this script with "
            f"`uv run {Path(__file__).name} ...` (installs it automatically) "
            f"or `pip install pypdf`."
        )
    reader = PdfReader(str(path))
    pages = []
    for i, page in enumerate(reader.pages, 1):
        text = (page.extract_text() or "").strip()
        if text:
            pages.append(f"### Page {i}\n\n{text}")
    if not pages:
        return (
            "_No extractable text. This is likely a scanned PDF — "
            "supply the notes in another format._"
        )
    return "\n\n".join(pages)


def read_gdoc(path):
    """Emit the Google Docs URL for the caller to fetch; there is no local text."""
    try:
        stub = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise SystemExit(f"{path.name} is not a readable .gdoc stub.")
    url = stub.get("url") or stub.get("URL")
    if not url and stub.get("doc_id"):
        url = f"https://docs.google.com/document/d/{stub['doc_id']}/edit"
    if not url:
        raise SystemExit(f"{path.name} contains no document URL.")
    return (
        f"GDOC_URL: {url}\n\n"
        "_This .gdoc file is a link stub, not the document text. Fetch the URL above. "
        "If it is private and cannot be fetched, ask for a .docx or .pdf export._"
    )


READERS = {
    ".md": read_text,
    ".txt": read_text,
    ".docx": read_docx,
    ".xlsx": read_xlsx,
    ".pdf": read_pdf,
    ".gdoc": read_gdoc,
}


def main():
    parser = argparse.ArgumentParser(
        description="Extract meeting notes from mixed formats into one markdown stream."
    )
    parser.add_argument("files", nargs="+", help=f"note files ({' '.join(SUPPORTED)})")
    args = parser.parse_args()

    chunks = []
    for name in args.files:
        path = Path(name).expanduser()
        if not path.is_file():
            raise SystemExit(f"Not a file: {path}")
        reader = READERS.get(path.suffix.lower())
        if reader is None:
            raise SystemExit(
                f"Unsupported format '{path.suffix}' for {path.name}. "
                f"Supported: {', '.join(SUPPORTED)}."
            )
        body = reader(path).strip()
        chunks.append(
            f"## {path.name}\n\n{body or '_(empty)_'}"
        )

    print("\n\n---\n\n".join(chunks))


if __name__ == "__main__":
    main()
