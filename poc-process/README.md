# poc-process

Proof of Concept artifact generation tools for Claude Code.

**Plugin version:** 0.2.0

PoC working state is kept as local markdown files in the repo under `pocs/<customer>/`, so artifacts stay versionable and readable without external services.

## Skills

### creating-poc-scoping-deck (v0.1.0)

Turn discovery notes into the Datadog-branded deck you present to a prospect to scope a Proof of Concept, built on the bundled 2026 PoC Scoping Template. Reads meeting notes in `.gdoc`, `.md`, `.txt`, `.docx`, `.xlsx` and `.pdf`, fills the template's placeholders with content grounded in those notes, and asks rather than invents when the notes fall short. Alongside the deck it writes a `scoping.md` summary and an `open-questions.md` list, so every remaining blank is a question you can send to the prospect. Also adds the tech-stack and timeline slides the template promises but omits, and rewrites the deck's URLs for the prospect's Datadog site.

**Example prompts:**
- "Create a PoC scoping deck for Northwind Bank from these discovery notes"
- "Turn my meeting notes into a POC scoping presentation"
- "Build the scoping deck for next week's proof-of-concept kick-off with this prospect"

**Prerequisites:** `python3`, plus `uv` (recommended) or `pip install defusedxml lxml Pillow` for the PPTX tooling. Reading `.pdf` notes needs `pypdf`, which `uv run` installs automatically. LibreOffice (`soffice`) and Poppler (`pdftoppm`) are optional and only used for the visual check; without them the skill falls back to text-level QA. The template and scripts are bundled under `skills/creating-poc-scoping-deck/assets/` and `skills/creating-poc-scoping-deck/scripts/`.
