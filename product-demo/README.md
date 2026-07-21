# product-demo

Product demo content generation tools for Claude Code.

## Skills

### create-pptx

Create a Datadog-branded product demo PowerPoint from meeting notes, built on the bundled 2026 Datadog Presentation Template. Follows a fixed 20-slide customer-demo flow and runs a mandatory visual QA loop.

**Example prompts:**
- "Create a demo deck from these meeting notes for ACME Corp"
- "Turn my meeting notes into a Datadog demo presentation"
- "Build a customer demo pptx covering their 3 challenges and our use cases"

**Prerequisites:** `python3`, `markitdown[pptx]`, `Pillow`, LibreOffice (`soffice`), and Poppler (`pdftoppm`). The editing scripts and template are bundled under `skills/create-pptx/scripts/` and `skills/create-pptx/assets/`.
