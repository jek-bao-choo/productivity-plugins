---
name: "converting-evalplan-to-tmap"
description: "Convert Evaluation Plan CSV files (creating-eval-plan 4-column output or Homerun 10-column export) into a TMAP (Technical Mutual Activity Plan) XLSX. Default output is Jek's customer-facing 5-column layout (Configuration Item, Responsible Party, Target Completion Date as Excel Short Date, Status with In Progress/Blocked/Complete colours, Notes) with descriptive track sections and a lean task list; the official 7-column ENT/MM template is produced only when asked for by name. Use when the user asks to convert an eval plan to TMAP, generate or update a TMAP XLSX, convert CSV to TMAP, or mentions \"TMAP\", \"mutual action plan\", \"Tech Config Plan\" or \"convert eval plan to xlsx\"."
---

# Evaluation Plan to TMAP Converter

Convert an Evaluation Plan CSV into a TMAP (Technical Mutual Activity Plan) XLSX. The TMAP is the customer-facing working plan. The full detail stays in the eval-plan CSV (Home Run) and the implementation guide, so the TMAP is a curated, leaner view.

There are two output modes:

| Mode | When | Spec |
|---|---|---|
| **Default: user's layout** | Always, unless the user names the official template | This file, "Default layout" below |
| **Official ENT/MM template** | User asks for the "official", "standard", "ENT/MM" or "7-column" TMAP | "Official template mode" below and `references/tmap-format-spec.md` |

## Supported Input Formats

### Format A: creating-eval-plan output (4 columns)

```
Depth,Title,Description,Success Criteria
```

`Depth` encodes the hierarchy (`1`, `1.1`, `1.1.1`).

### Format B: Homerun export (10 columns)

```
Depth Value,Status,Assignee,Due Date,Status Text,Roll up children's status,Name,Description,Success Criteria,Shared
```

Detect the format from the header row: `Depth,Title,Description,Success Criteria` is Format A; `Depth Value,Status,Assignee,Due Date` is Format B.

| Target | Format A source | Format B source |
|---|---|---|
| Title | `Title` | `Name` |
| Description | `Description` | `Description` |
| Success Criteria | `Success Criteria` | `Success Criteria` |
| Status | `Open` | `Status`: `Complete` stays `Complete`; `In Progress` and `Blocked` are kept; anything else becomes `Open` |
| Responsible Party | from the source plan or ask; never invent names | `Assignee` (drop `Not Assigned`) |
| Target Completion Date | from the source plan or ask | `Due Date` (drop `No due date`) |

If owners or dates are missing, ask the user (or take them from the conversation or plan data). Do not leave every row blank without saying so.

---

## Default layout

### Sheet `Tech Config Plan`: columns

| Col | Header | Width |
|---|---|---|
| A | Configuration Item | 53.7 |
| B | Responsible Party | 23.2 |
| C | Target Completion Date | 31.3 |
| D | Status | 12.3 |
| E | Notes | 70 |

There is no Product Category column, no Estimated Complete Time column, and no merged category cells.

- Header row: bold white text on purple `674EA7`, wrap text, top-aligned. Freeze panes at `A2`.
- All cells: wrap text, vertical top. Item rows have thin light-grey borders (`D9D9D9`).

### Section rows (depth 1)

- Use descriptive section names and drop any `Phase N:` prefix. Typical sections:
  - `Pre-req: Housekeeping, Scope, and Success Criteria`. Merge scoping and access, network and change readiness into this one section.
  - `Track A - <System> UAT Instrumentation (<OS> / <web server> / <DB>)`
  - `Track A - Dashboards & Bits AI`
  - `Track A - <System> Production Rollout`
  - `Track B - <System>: <focus>` when there is a second parallel track
  - `PoC Review & Close`
- Fill all five cells with purple `9900FF`, bold white text. Every section row is the same purple; there is no blue row.
- Column C holds the section's **end date** as a real date (see Dates). Column E holds `Window: <Ddd dd/mm/yyyy> - <Ddd dd/mm/yyyy>`.

### Item rows (depth 2 and deeper)

- Depth-2 category rows that have children are **not** written as rows. Their children follow directly under the section. A depth-2 row without children is an ordinary item.
- A: title. B: owner(s). C: date. D: status. E: notes.
- Notes: `{Description} | {Success Criteria}`, or just whichever one exists.
- Titles starting with `CRITICAL` get bold dark-red text (`CC0000`).

### Content curation (customer-facing)

Apply these rules when building the TMAP from a detailed plan. Mention in your report what you dropped or merged.

1. Keep only tasks someone has to act on.
2. Drop `(Informational)`, `[Informational]` and `(Debug)` rows, and items already confirmed or completed before the TMAP is issued.
3. Leave out internal or commercial items: RFQ or scoring templates, renewal timing, competitive or Datadog positioning statements, CVE or security-exposure assessments, scope-exclusion notes. These belong in internal notes, not the customer's working plan.
4. Merge fine-grained setup rows into outcome rows. For example, one `Build the <System> End-to-End Dashboard` row, one `Build the <System> Database Health Dashboard` row, and one `Use Bits AI for <Customer> use cases` row, instead of separate monitor, SLO and Bits configuration rows.
5. Keep success-criteria rows (`Agree Track A (...) Success Criteria`) but leave their Notes blank, because the criteria are agreed live with the customer.
6. List the Datadog AE alongside the SE as responsible party on scoping, SME-session and success-criteria rows.
7. Keep the order the user gives. If the user reorders sections, keep their order.

### Dates (column C): real Excel Short Dates

Every value in column C must be a real date, never text.

- Parse dates **day-first** (`dd/mm/yyyy`; the user works in Southeast Asia). A short `dd/mm` takes the year of the last full date in the same cell.
- If a weekday name is present (`Fri 16/10/2026`), check it matches the parsed date. Stop and report any mismatch rather than guessing.
- **Range** (`Tue 06/10 - Fri 16/10/2026`): write the end date. Prepend `Window: <start> - <end>` to Notes.
- **Raise / ready** (`Raise Wed 07/10; ready Fri 16/10/2026`): write the ready date. Prepend `Raise by <date>` to Notes.
- Number format `mm-dd-yy`. In openpyxl this maps to Excel built-in `numFmtId 14`, which is Excel's Short Date and displays in the viewer's regional format. Verify in `xl/styles.xml` that column C cells use `numFmtId="14"`.

```python
import re, datetime as dt
TOKEN = re.compile(r"(?:(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+)?(\d{1,2})/(\d{1,2})(?:/(\d{4}))?")

def parse_dates(text):
    toks = list(TOKEN.finditer(text))
    years = [int(m.group(4)) for m in toks if m.group(4)]
    out = []
    for m in toks:
        d = dt.date(int(m.group(4)) if m.group(4) else years[-1], int(m.group(3)), int(m.group(2)))
        if m.group(1) and d.strftime("%a") != m.group(1):
            raise ValueError(f"weekday mismatch: {text!r}")
        out.append(d)
    return out

# cell.value = target_date ; cell.number_format = "mm-dd-yy"   # built-in 14 = Short Date
```

### Status (column D): dropdown and colours

- Data validation list: `Open,In Progress,Complete,Blocked`. Use `Complete`, not `Completed`.
- Conditional formatting on `D2:D1000`, cell value equal to:

| Value | Fill | Font |
|---|---|---|
| `In Progress` | yellow `FFEB9C` | `9C5700` |
| `Blocked` | red `FFC7CE` | `9C0006` |
| `Complete` | green `C6EFCE` | `006100` |

```python
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import PatternFill, Font
for value, bg, fg in [("In Progress","FFFFEB9C","FF9C5700"),("Blocked","FFFFC7CE","FF9C0006"),("Complete","FFC6EFCE","FF006100")]:
    ws.conditional_formatting.add("D2:D1000", CellIsRule(operator="equal", formula=[f'"{value}"'],
        fill=PatternFill(start_color=bg, end_color=bg, fill_type="solid"), font=Font(color=fg)))
```

### Supporting sheets (when the plan has the content)

- **`Scope & Owners`**: only two blocks.
  1. Section title `Owners` (merged A:D, purple `9900FF`, bold white), then a table `Area | Owner | Track | Notes`. The table header is bold on light grey `F3F3F3`, rows have thin borders.
  2. Section title `Call-outs and risks` (same style), then a two-column table `Call-out | Action`.
  - No title banner, tracks table or timeline table.
- **`<SME name> Session Questions`**: columns `Area | Question | Why it matters | Answer (fill in during session)`. No `#` column. Header `674EA7` bold white; freeze `A2`.

### Updating an existing TMAP the user has edited

- Load the user's file and change only what was asked. Keep their rows, wording, order, widths and styles.
- Back up the file before writing. Diff before and after, and report which cells changed.
- Excel holds a `~$<name>.xlsx` lock file while the workbook is open. If it exists, warn the user that saving in Excel would overwrite your changes.

---

## Official template mode (only when asked)

Produce the official Datadog ENT/MM Mutual Action Plan layout. Read `references/tmap-format-spec.md`.

- Sheet `Tech Config Plan`, 7 columns: Product Category (20.33), Configuration Item (53.66), Estimated Complete Time (13.66), Responsible Party (23.16), Target Completion Date (24.16), Status (21.83), Notes (35.16). Header bold white on `674EA7`.
- Phase rows (depth 1): A = `Phase N` (from `Phase N:` in the title, otherwise its position starting at 0), B = title without the prefix. Bold white; Phase 1 blue `1E82FF`, all others purple `9900FF`.
- Category rows (depth 2 with children): A = category name, bold on `F3F3F3`, merged down across its child rows; the first child shares the row. Depth-2 rows without children are items with A blank.
- Items: B title, D owner, E date, F `Open`/`Complete`, G notes `{Description} | {Success Criteria}`.
- Even in this mode, write Target Completion Date as a real Short Date and add the status colours, unless the user says otherwise.

---

## Workflow

1. Read the CSV and detect Format A or B.
2. Parse the hierarchy and map the fields.
3. Choose the mode (default unless the official template is named).
4. In default mode, apply content curation and keep a list of what was merged or dropped.
5. Write an openpyxl script (`pip3 install openpyxl` if missing) and run it with `python3`.
6. Save to the path the user gives, or next to the input CSV as `TMAP_<Customer>_<scope>.xlsx`.
7. Validate:
   - The file opens.
   - Section rows are purple with bold white text.
   - Column C cells are numeric dates with `numFmtId 14` and no text remains.
   - Weekday names matched their dates.
   - The status dropdown and the three colour rules are present on column D.
   - Notes carry the description and success criteria where they exist.
8. Report: output path; counts of sections and items; what was curated out; any date conversions that moved text into Notes; any warnings.

