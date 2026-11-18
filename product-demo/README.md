# product-demo

Product demo content generation tools for Claude Code.

**Plugin version:** 0.4.0

## Skills

### creating-demo-deck (v0.5.0)

Create a Datadog-branded product demo deck from meeting notes, as the last step of a three-stage pipeline: first `answering-rfp` (sales-process plugin) turns the notes into an RFP response CSV that states, for every known tech stack item, whether Datadog supports it; then `creating-solution-architecture` draws the architecture from the notes and the RFP output; then the deck is built as a Claude Artifact using its Datadog presentation styles. The skill carries the structure of the 2026 Datadog Presentation Template (28-slide flow, layouts, palette, type) as instructions. The deck opens with a six-part agenda table (Intro & Whiteboard, Observe, Act, Secure, Why Datadog, Next Steps & Close), adds the architecture diagram in the Intro & Whiteboard part, returns to the agenda as a benefits tracker after each part, and ends with a "Your stack on Datadog" backup slide that covers every tech stack row in the RFP CSV. The deck never claims more than the RFP says. All text follows concise word limits (rule of 3, short fragments, no filler), checked in a mandatory review.

**Example prompts:**
- "Create a demo deck from these meeting notes for ACME Corp"
- "Turn my meeting notes into a Datadog demo presentation"
- "Build a customer demo pptx covering their 3 challenges and our use cases"

**Prerequisites:** the `sales-process` plugin (for `answering-rfp`), `creating-solution-architecture` from this plugin, and Claude Artifacts with the Datadog presentation styles. No scripts or template files: the skill is a single `SKILL.md`.

### creating-solution-architecture (v0.6.0)

Design an end-to-end Datadog monitoring architecture from sales discovery notes and technical plans, and render it as a diagram in Excalidraw. Delivers two matching files: an editable `.excalidraw` scene and a `.svg` diagram for slides, docs and Slack. Draws a current state view (fragmented monitoring tools, silos and pain points) above a target state view (consolidated on Datadog), both flowing left to right from the customer environment to the destination. Covers Infrastructure/Application/UI layers, a per-signal telemetry transmission breakdown (metrics, traces/spans, logs, alert and other events) with the protocol and port for every hop to the Datadog SaaS intake (EU/US/AP), collection methods (Agent, Cluster Agent, OpenTelemetry Collector, API integrations), and security/networking overlays (proxy, firewall, PrivateLink). It only draws a telemetry flow when every hop is confirmed to work; anything uncertain or not possible (unsupported runtime, unknown egress, air-gapped network) is left off the diagram and called out in a "Not drawn: needs confirmation" box instead.

**Example prompts:**
- "Design a Datadog architecture diagram for this customer's K8s environment"
- "Turn these discovery notes into an Excalidraw diagram of their monitoring setup"
- "Map out the data flow for metrics, traces, and logs to our EU region"
- "Show which protocols and ports each telemetry flow uses so the firewall team can review it"
- "Draw their current fragmented monitoring vs the consolidated Datadog target state"

**Prerequisites:** none bundled — the skill looks for an Excalidraw MCP connector and an Anthropic-provided "architecture" skill at runtime and uses them if present, otherwise it falls back to generating a `.excalidraw` JSON scene file you can import manually. The `.svg` export needs `python3`; Google Chrome (or macOS `qlmanage`) is used to preview it. The full design framework, including default Datadog protocols and ports, lives in the skill's `SKILL.md`.
