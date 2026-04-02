# TMAP XLSX Format Specification

Extracted from `Official_Standard_ENT_MM_Mutual_Action_Plan.xlsx`. This spec enables programmatic generation of the XLSX without reading the binary template.

## Sheet

- Sheet name: `Tech Config Plan`

## Columns

| Column | Header | Width |
|--------|--------|-------|
| A | Product Category | 20.33 |
| B | Configuration Item | 53.66 |
| C | Estimated Complete Time | 13.66 |
| D | Responsible Party | 23.16 |
| E | Target Completion Date | 24.16 |
| F | Status | 21.83 |
| G | Notes | 35.16 |

## Row Types

### 1. Header Row (Row 1)

- All columns filled with header text
- Font: **Bold**, color white (`FFFFFF`)
- Background: purple `FF674EA7`

### 2. Phase Row

A phase row marks the start of a major section (Phase 0, 1, 2, 3, etc.).

- **Column A**: `Phase N` (where N is the phase index starting from 0)
- **Column B**: Phase title (e.g., "Sign up For Trial", "Configuration / Data Collection", "Datadog UI", "POV Review")
- Font: **Bold**, color white (`FFFFFF`)
- Background colors by phase index:
  - Phase 0: purple `FF9900FF`
  - Phase 1: blue `FF1E82FF`
  - Phase 2: purple `FF9900FF`
  - Phase 3: purple `FF9900FF`
  - Phase 4+: purple `FF9900FF` (default)
- Columns C through G: empty

### 3. Category Row

A category groups related configuration items under a product area.

- **Column A**: Category name (e.g., "On-Prem", "AWS", "APM - .NET", "Log Collection", "Dashboards & Visualizations")
- Font in A: **Bold**
- Background in A: light grey `FFF3F3F3`
- **Column A is merged** vertically across all item rows that belong to this category (from the first item row to the last item row under this category)
- Only depth-2 rows that have depth-3+ children are categories. Depth-2 rows without children are standalone items (see Item Row below).
- Columns B through G: the first item row shares this row (i.e., the first child item appears on the same row as the category)

### 4. Item Row

An individual configuration/task item.

- **Column A**: empty (or part of the merged category cell)
- **Column B**: Item title
- **Column C**: Estimated time (if available, otherwise empty)
- **Column D**: Responsible party (if available, otherwise empty)
- **Column E**: Target date (if available, otherwise empty)
- **Column F**: Status ("Open" or "Complete")
- **Column G**: Notes (Description and/or Success Criteria)
- Font: normal (not bold)
- No background color

## Status Values

- `Open` (default for all items)
- `Complete`

## Notes Column Format

When combining Description and Success Criteria:
- If both present: `{Description} | {Success Criteria}`
- If only Description: `{Description}`
- If only Success Criteria: `{Success Criteria}`
- If neither: empty

## Phase Title Mapping

The CSV depth-1 titles often include "Phase N:" prefix. The XLSX splits this:
- CSV: `Phase 0: Scoping & Alignment` → XLSX Col A: `Phase 0`, Col B: `Scoping & Alignment`
- CSV: `Phase 2: Datadog Setup & Data Collection` → XLSX Col A: `Phase 2`, Col B: `Datadog Setup & Data Collection`

If the CSV title does not contain "Phase", derive the phase number from its position (first depth-1 = Phase 0, second = Phase 1, etc.) and use the full title as Col B.
