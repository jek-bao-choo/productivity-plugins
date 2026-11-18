# product-demo

Product demo content generation tools for Claude Code.

**Plugin version:** 0.4.0

## Skills

### creating-demo-pptx (v0.3.0)

Create a Datadog-branded product demo PowerPoint from meeting notes, built on the bundled 2026 Datadog Presentation Template. Follows a fixed 26-slide customer-demo flow that opens with a six-part agenda table (Intro & Whiteboard, Observe, Act, Secure, Why Datadog, Next Steps & Close) built by `build_agenda.py`, and runs a mandatory visual QA loop. The agenda's third column shows customer questions when the notes have them, otherwise points from your notes. After each part, a benefits tracker repeats the table with the benefits to the customer so far, highlighting the part just covered. All deck text follows concise word limits (rule of 3, short fragments, no filler), checked by `check_wording.py`. Finishes by invoking the `creating-architecture-via-excalidraw` skill on the same discovery notes to also produce a matching Datadog architecture diagram.

**Example prompts:**
- "Create a demo deck from these meeting notes for ACME Corp"
- "Turn my meeting notes into a Datadog demo presentation"
- "Build a customer demo pptx covering their 3 challenges and our use cases"

**Prerequisites:** `python3`, `markitdown[pptx]`, `Pillow`, LibreOffice (`soffice`), and Poppler (`pdftoppm`). The editing scripts and template are bundled under `skills/creating-demo-pptx/scripts/` and `skills/creating-demo-pptx/assets/`.

### creating-architecture-via-excalidraw (v0.4.0)

Design an end-to-end Datadog monitoring architecture from sales discovery notes and technical plans, and render it as a diagram in Excalidraw. Delivers two matching files: an editable `.excalidraw` scene and a `.svg` diagram for slides, docs and Slack. Draws a current state view (fragmented monitoring tools, silos and pain points) above a target state view (consolidated on Datadog), both flowing left to right from the customer environment to the destination. Covers Infrastructure/Application/UI layers, a per-signal telemetry transmission breakdown (metrics, traces/spans, logs, alert and other events) with the protocol and port for every hop to the Datadog SaaS intake (EU/US/AP), collection methods (Agent, Cluster Agent, OpenTelemetry Collector, API integrations), and security/networking overlays (proxy, firewall, PrivateLink). It only draws a telemetry flow when every hop is confirmed to work; anything uncertain or not possible (unsupported runtime, unknown egress, air-gapped network) is left off the diagram and called out in a "Not drawn: needs confirmation" box instead.

**Example prompts:**
- "Design a Datadog architecture diagram for this customer's K8s environment"
- "Turn these discovery notes into an Excalidraw diagram of their monitoring setup"
- "Map out the data flow for metrics, traces, and logs to our EU region"
- "Show which protocols and ports each telemetry flow uses so the firewall team can review it"
- "Draw their current fragmented monitoring vs the consolidated Datadog target state"

**Prerequisites:** none bundled — the skill looks for an Excalidraw MCP connector and an Anthropic-provided "architecture" skill at runtime and uses them if present, otherwise it falls back to generating a `.excalidraw` JSON scene file you can import manually. The `.svg` export needs `python3`; Google Chrome (or macOS `qlmanage`) is used to preview it. The full design framework, including default Datadog protocols and ports, lives in the skill's `SKILL.md`.
