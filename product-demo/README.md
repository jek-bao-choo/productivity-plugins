# product-demo

Product demo content generation tools for Claude Code.

**Plugin version:** 0.3.0

## Skills

### create-demo-pptx (v0.2.0)

Create a Datadog-branded product demo PowerPoint from meeting notes, built on the bundled 2026 Datadog Presentation Template. Follows a fixed 20-slide customer-demo flow and runs a mandatory visual QA loop. Finishes by invoking the `create-architecture-excalidraw` skill on the same discovery notes to also produce a matching Datadog architecture diagram.

**Example prompts:**
- "Create a demo deck from these meeting notes for ACME Corp"
- "Turn my meeting notes into a Datadog demo presentation"
- "Build a customer demo pptx covering their 3 challenges and our use cases"

**Prerequisites:** `python3`, `markitdown[pptx]`, `Pillow`, LibreOffice (`soffice`), and Poppler (`pdftoppm`). The editing scripts and template are bundled under `skills/create-demo-pptx/scripts/` and `skills/create-demo-pptx/assets/`.

### create-architecture-excalidraw (v0.2.0)

Design an end-to-end Datadog monitoring architecture from sales discovery notes and technical plans, and render it as a diagram in Excalidraw. Covers Infrastructure/Application/UI layers, metrics/traces/logs data flow to the Datadog SaaS intake (EU/US/AP), collection methods (Agent, Cluster Agent, OpenTelemetry Collector, API integrations), and security/networking overlays (proxy, firewall, PrivateLink).

**Example prompts:**
- "Design a Datadog architecture diagram for this customer's K8s environment"
- "Turn these discovery notes into an Excalidraw diagram of their monitoring setup"
- "Map out the data flow for metrics, traces, and logs to our EU region"

**Prerequisites:** none bundled — the skill looks for an Excalidraw MCP connector and an Anthropic-provided "architecture" skill at runtime and uses them if present, otherwise it falls back to generating a `.excalidraw` JSON scene file you can import manually. See `skills/create-architecture-excalidraw/references/architecture-checklist.md` for the design framework.
