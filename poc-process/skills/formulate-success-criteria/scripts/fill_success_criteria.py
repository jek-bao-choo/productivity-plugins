#!/usr/bin/env python3
"""Fill the success-criteria .xlsx template with customer rows.

Stdlib only (no pip installs). Copies the blank template shipped with this
skill and appends one row per entry, preserving the template's styling,
column widths, and branded logo.

Input JSON: a list of objects with these keys (all optional strings):
    - success_criteria   -> column C
    - current_challenge  -> column D
    - future_state       -> column E
    - products           -> column F ("Product(s) Tested")

Columns G (Validated Y/N) and H (In-app Recording) are intentionally left
blank for the SE to fill in later.

Usage:
    python3 fill_success_criteria.py --rows rows.json --output out.xlsx
    python3 fill_success_criteria.py --rows rows.json --output out.xlsx \
        --template /path/to/success-criteria-template.xlsx
"""
import argparse
import json
import os
import re
import zipfile

SHEET = "xl/worksheets/sheet1.xml"
HEADER_ROW = 3  # data starts on row 4

# Style ids captured from the template (see styles.xml cellXfs):
#   s=2 -> left spacer column B
#   s=5 -> data cell (border, vertical top, wrapText)
#   s=6 -> trailing cells G/H (Validated Y/N, In-app Recording)
STYLE_SPACER = "2"
STYLE_DATA = "5"
STYLE_TRAILING = "6"


def xml_escape(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def estimate_height(fields):
    """Rough row height so wrapped multi-line content is visible on open."""
    max_lines = 1
    for value in fields:
        if not value:
            continue
        # Count explicit newlines plus a crude wrap estimate for long lines.
        lines = 0
        for line in value.split("\n"):
            lines += max(1, (len(line) // 45) + 1)
        max_lines = max(max_lines, lines)
    return min(409.6, max(15.75, max_lines * 14.0))


def cell(ref, style, text):
    if text:
        return (
            '<c r="{ref}" s="{s}" t="inlineStr"><is><t xml:space="preserve">'
            "{txt}</t></is></c>"
        ).format(ref=ref, s=style, txt=xml_escape(text))
    return '<c r="{ref}" s="{s}"/>'.format(ref=ref, s=style)


def build_row(row_num, entry):
    sc = (entry.get("success_criteria") or "").strip()
    cc = (entry.get("current_challenge") or "").strip()
    fs = (entry.get("future_state") or "").strip()
    pr = (entry.get("products") or "").strip()
    height = estimate_height([sc, cc, fs, pr])
    cells = [
        cell("B{}".format(row_num), STYLE_SPACER, ""),
        cell("C{}".format(row_num), STYLE_DATA, sc),
        cell("D{}".format(row_num), STYLE_DATA, cc),
        cell("E{}".format(row_num), STYLE_DATA, fs),
        cell("F{}".format(row_num), STYLE_DATA, pr),
        cell("G{}".format(row_num), STYLE_TRAILING, ""),
        cell("H{}".format(row_num), STYLE_TRAILING, ""),
    ]
    return (
        '<row r="{r}" spans="1:26" ht="{h}" customHeight="1" '
        'x14ac:dyDescent="0.15">{cells}</row>'
    ).format(r=row_num, h=height, cells="".join(cells))


def fill(template_path, rows, output_path):
    with zipfile.ZipFile(template_path) as z:
        names = z.namelist()
        data = {n: z.read(n) for n in names}
        infos = {n: z.getinfo(n) for n in names}

    sheet = data[SHEET].decode("utf-8")

    new_rows = []
    row_num = HEADER_ROW
    for entry in rows:
        row_num += 1
        new_rows.append(build_row(row_num, entry))
    last_row = row_num

    # Insert the new rows just before </sheetData>.
    if "</sheetData>" not in sheet:
        raise ValueError("Unexpected sheet XML: missing </sheetData>")
    sheet = sheet.replace("</sheetData>", "".join(new_rows) + "</sheetData>", 1)

    # Widen the sheet dimension to cover the appended rows.
    sheet = re.sub(
        r'<dimension ref="A1:[A-Z]+\d+"/>',
        '<dimension ref="A1:Z{}"/>'.format(last_row),
        sheet,
        count=1,
    )

    data[SHEET] = sheet.encode("utf-8")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as z:
        for name in names:
            info = infos[name]
            zi = zipfile.ZipInfo(name, date_time=info.date_time)
            zi.compress_type = info.compress_type
            zi.external_attr = info.external_attr
            z.writestr(zi, data[name])

    return last_row - HEADER_ROW


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", required=True, help="Path to rows JSON file")
    parser.add_argument("--output", required=True, help="Path to output .xlsx")
    default_template = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "references",
        "success-criteria-template.xlsx",
    )
    parser.add_argument(
        "--template",
        default=default_template,
        help="Path to the blank template (defaults to the one shipped with this skill)",
    )
    args = parser.parse_args()

    with open(args.rows, "r", encoding="utf-8") as f:
        rows = json.load(f)
    if not isinstance(rows, list):
        raise ValueError("Rows JSON must be a list of objects")

    count = fill(args.template, rows, args.output)
    print("Wrote {} row(s) to {}".format(count, args.output))


if __name__ == "__main__":
    main()
