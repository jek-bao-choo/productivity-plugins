# product-demo

Product demo content generation tools for Claude Code.

**Plugin version:** 0.8.0

## Skills

### creating-demo-deck (v0.7.1)

Create a Datadog-branded product demo deck from meeting notes, as the last step of a three-stage pipeline: first `answering-rfp` (sales-process plugin) turns the notes into an RFP response sheet (Claude Artifact Sheets, or `.csv`) that states, for every known tech stack item, whether Datadog supports it; then `creating-solution-architecture` draws the architecture from the notes and the RFP output; then the deck is built with Claude Artifact Slides in its Datadog presentation styles (top preference), falling back to one self-contained HTML deck only when Claude Artifacts aren't available, which you then drop into Claude Artifacts to make the Slides deck. It never builds PowerPoint. The skill carries the structure of the 2026 Datadog Presentation Template (28-slide flow, layouts, palette, type) as instructions. The deck opens with a six-part agenda table (Intro & Whiteboard, Observe, Act, Secure, Why Datadog, Next Steps & Close), adds the architecture diagram in the Intro & Whiteboard part, returns to the agenda as a benefits tracker after each part, and ends with a "Your stack on Datadog" backup slide that covers every tech stack row in the RFP sheet. The deck never claims more than the RFP says. All text follows concise word limits (rule of 3, short fragments, no filler), checked in a mandatory review.

**Example prompts:**
- "Create a demo deck from these meeting notes for ACME Corp"
- "Turn my meeting notes into a Datadog demo presentation"
- "Build a customer demo deck covering their 3 challenges and our use cases"

**Prerequisites:** the `sales-process` plugin (for `answering-rfp`), `creating-solution-architecture` from this plugin, and Claude Artifact Slides with the Datadog presentation styles (checked at runtime; without it the skill writes an HTML deck, previewed with Google Chrome). No scripts or template files: the skill is a single `SKILL.md`.

### creating-solution-architecture (v0.8.0)

Design an end-to-end Datadog monitoring architecture from sales discovery notes and technical plans, and draw it with Claude Artifact Design (top preference), falling back to a hybrid HTML file (HTML and CSS boxes, inline SVG arrows) plus a `.png` render only when Claude Artifacts aren't available; you then drop the HTML into Claude Artifact Design. Never uses Excalidraw. Draws a current state view (fragmented monitoring tools, silos and pain points) above a target state view (consolidated on Datadog), both flowing left to right from the customer environment to the destination. Covers Infrastructure/Application/UI layers, a per-signal telemetry transmission breakdown (metrics, traces/spans, logs, alert and other events) with the protocol and port for every hop to the Datadog SaaS intake (EU/US/AP), collection methods (Agent, Cluster Agent, OpenTelemetry Collector, API integrations), and security/networking overlays (proxy, firewall, PrivateLink). It only draws a telemetry flow when every hop is confirmed to work; anything uncertain or not possible (unsupported runtime, unknown egress, air-gapped network) is left off the diagram and called out in a "Not drawn: needs confirmation" box instead.

**Example prompts:**
- "Design a Datadog architecture diagram for this customer's K8s environment"
- "Turn these discovery notes into an architecture diagram of their monitoring setup"
- "Map out the data flow for metrics, traces, and logs to our EU region"
- "Show which protocols and ports each telemetry flow uses so the firewall team can review it"
- "Draw their current fragmented monitoring vs the consolidated Datadog target state"

**Prerequisites:** Claude Artifacts with Design (checked at runtime); without it the skill writes the hybrid HTML itself. Google Chrome renders the `.png`, and `python3` runs the wording check. The full design framework, including default Datadog protocols and ports, lives in the skill's `SKILL.md`.
