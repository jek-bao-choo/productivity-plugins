# poc-process

Proof of Concept artifact generation tools for Claude Code.

**Plugin version:** 0.3.0

PoC working state is kept as local markdown files in the repo under `pocs/<customer>/`, so artifacts stay versionable and readable without external services.

## Skills

### creating-eval-plan (v0.4.0)

Generate a modular Evaluation Plan CSV for Datadog Home Run PoC/Trial management. Combines solution-area modules (Infrastructure, APM, Logs, Cloud SIEM, LLM Observability, NDM, RUM, Synthetics, CCM, Security, DBM, Incident Management, Bits AI, Service Management) into a 4-column CSV (Depth, Title, Description, Success Criteria) ready for upload to Home Run, with version-specific titles for the prospect's languages, OSes and databases. Can also produce an implementation guide from the bundled `IMPLEMENTATION_GUIDE.md` template.

**Usage:** `/poc-process:creating-eval-plan`

**Example prompts:**
- "Create an evaluation plan for ACME Corp with Infrastructure and APM"
- "Generate an eval plan for Cloud SIEM evaluation"
- "Build a comprehensive evaluation plan covering APM, Logs, and Infrastructure for CustomerX"

### converting-evalplan-to-tmap

Convert an Evaluation Plan CSV (the 4-column `creating-eval-plan` output or a 10-column Home Run export) into a TMAP (Technical Mutual Activity Plan) XLSX. The default output is a lean, customer-facing 5-column layout (Configuration Item, Responsible Party, Target Completion Date, Status, Notes) with descriptive track sections. The official 7-column ENT/MM template is produced only when asked for by name.

**Usage:** `/poc-process:converting-evalplan-to-tmap`

**Example prompts:**
- "Convert this eval plan CSV to a TMAP"
- "Generate the mutual action plan XLSX for ACME from their Home Run export"
- "Build the official ENT/MM TMAP from this evaluation plan"

**Prerequisites:** `python3` with `openpyxl` (`pip3 install openpyxl`).

### formulate-success-criteria (v0.1.0)

Turn customer meeting notes and/or call transcripts into a filled copy of the bundled 2025 success criteria `.xlsx` template, with one row per criterion across Success Criteria, Current Challenge, Future State and Product(s) Tested. Current challenges are grounded in what the customer actually said, success criteria are outcome-based, and the skill asks clarifying questions when the notes are unclear. Rows are previewed as a Markdown table for review before the workbook is written.

**Usage:** `/poc-process:formulate-success-criteria`

**Example prompts:**
- "Formulate success criteria for Northwind Bank from these meeting notes"
- "Turn this call transcript into current challenges and future states"
- "Fill the success criteria spreadsheet for our upcoming POC with ACME"

**Prerequisites:** `python3` (the fill script uses only the standard library).

### creating-poc-scoping-deck (v0.1.2)

Turn discovery notes into the Datadog-branded deck you present to a prospect to scope a Proof of Concept, built on the bundled 2026 PoC Scoping Template. Reads meeting notes in `.gdoc`, `.md`, `.txt`, `.docx`, `.xlsx` and `.pdf`, fills the template's placeholders with content grounded in those notes, and asks rather than invents when the notes fall short. Alongside the deck it writes a `scoping.md` summary and an `open-questions.md` list, so every remaining blank is a question you can send to the prospect. Also adds the tech-stack and timeline slides the template promises but omits, and rewrites the deck's URLs for the prospect's Datadog site.

**Example prompts:**
- "Create a PoC scoping deck for Northwind Bank from these discovery notes"
- "Turn my meeting notes into a POC scoping presentation"
- "Build the scoping deck for next week's proof-of-concept kick-off with this prospect"

**Prerequisites:** `python3`, plus `uv` (recommended) or `pip install defusedxml lxml Pillow` for the PPTX tooling. Reading `.pdf` notes needs `pypdf`, which `uv run` installs automatically. LibreOffice (`soffice`) and Poppler (`pdftoppm`) are optional and only used for the visual check; without them the skill falls back to text-level QA. The template and scripts are bundled under `skills/creating-poc-scoping-deck/assets/` and `skills/creating-poc-scoping-deck/scripts/`.
