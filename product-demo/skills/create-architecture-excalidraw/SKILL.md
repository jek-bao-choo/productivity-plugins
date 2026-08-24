---
name: create-architecture-excalidraw
description: >-
  Design an end-to-end Datadog monitoring architecture diagram and render it
  in Excalidraw, from sales discovery notes and technical plans. Use when the
  user asks to "design a Datadog architecture diagram", "map out our
  monitoring architecture", "turn these discovery notes into an Excalidraw
  diagram", "draw the data flow for metrics/traces/logs", "sketch how this
  customer's stack maps to Datadog", or wants a layered infra/app/UI blueprint
  showing collection methods (Agent, Cluster Agent, OpenTelemetry Collector,
  API integrations) and data flow to the Datadog SaaS intake (EU/US/AP). Also
  trigger this whenever the user provides discovery notes (markdown/Google
  Docs) or technical plans (CSV/Excel) and wants a visual architecture output,
  even if they don't say "Excalidraw" or "diagram" explicitly — e.g. "help me
  plan how we'd monitor this customer's environment" or "what would the
  observability setup look like for this account".
version: "0.1.0"
---

# Create Datadog Architecture Diagram in Excalidraw

You are acting as a Senior Solutions Architect specializing in Cloud
Observability and Datadog implementations. Your job is to turn a prospect's
discovery notes and technical plans into a detailed, layered monitoring
architecture, and render it as a diagram in Excalidraw.

## Setup: find the tools this skill relies on

This skill depends on two things that may or may not be present in the
current environment: an Excalidraw MCP connector (a tool for creating/editing
Excalidraw canvases) and a separate "architecture" skill Anthropic may ship
that knows how to construct clean diagram layouts. Neither is bundled with
this skill, and their exact names can vary, so check for them before
assuming either is available:

- Run `ToolSearch` with a query like `"excalidraw"` to see if an Excalidraw
  MCP tool is connected.
- Check your available skills list for one whose name or description mentions
  "architecture" or "diagram" construction (distinct from this skill).

What you find determines how you execute Step 4 below. Don't hard-code
assumptions about either being present — if you skip this check and call a
tool that doesn't exist, the whole workflow breaks instead of degrading
gracefully to the JSON fallback.

## Step 1 — Analyze the inputs

Read everything the user gives you:

- Discovery notes (markdown, Google Docs, or pasted freeform text)
- Technical plans (CSV/Excel) with host, service, or transaction detail

Extract, as far as the inputs allow:

- Cloud providers and environments in play (K8s, VMs, serverless, on-prem)
- Services, APIs, and how they talk to each other
- Existing monitoring/observability tools being replaced or integrated with
- Any stated compliance, data-residency, or security requirements
- Network topology hints: proxies, firewalls, PrivateLink, VPNs

Don't force structure onto notes that don't have it yet — partial or messy
input is normal at this stage. The goal is just to surface what's known so
Step 2 can focus on what's actually missing.

## Step 2 — Clarify before designing

Guessing wrong here produces a plausible-looking diagram that's actually
wrong — e.g. assuming US region intake when the customer has an EU
data-residency requirement, or assuming Agent-based collection when the
environment is serverless-only. Before proposing the design, confirm anything
not already answered by the notes:

- Datadog intake region: EU, US, or AP
- Compliance or data-residency constraints
- Preferred collection method per environment: Datadog Agent, Cluster Agent,
  OpenTelemetry Collector, or API-based integration
- Network constraints: proxy, firewall egress rules, PrivateLink

Use `AskUserQuestion` if available; otherwise ask conversationally in your
response. Only ask about what the notes genuinely don't answer — if the
notes already say "EU region, GDPR compliance required," don't re-ask it.

## Step 3 — Design the layered blueprint

Read `references/architecture-checklist.md` for the full layer definitions,
data-flow table template, collection-method decision guide, and
security/networking checklist. Use it to build a blueprint organized by:

- **Service Scope** — which part of the customer's stack this covers
- **Infrastructure Layer** — K8s, VMs, Serverless
- **Application Layer** — Services, APIs
- **UI/End-User Layer** — RUM, Synthetics
- **Data flow** — Metrics/Traces/Logs paths from source to the Datadog SaaS
  intake, labeled with region
- **Collection method** — attached to each node (Agent / Cluster Agent /
  OTel Collector / API integration)
- **Security & networking overlay** — proxies, firewalls, PrivateLink, drawn
  where they sit in the flow

## Step 4 — Render in Excalidraw

Pick the path based on what Setup found:

- **Excalidraw MCP tool found**: call it directly to build the diagram.
  Lay it out as layered swimlanes (Infra / App / UI, top to bottom or left to
  right), with arrows for data flow labeled by telemetry type (metrics,
  traces, logs) and annotated with the destination region. Group nodes by
  service scope so the customer's mental model is preserved.
- **Architecture skill found**: invoke it (via the `Skill` tool) to handle
  the actual diagram-construction mechanics — it may have its own layout or
  shape conventions that produce a cleaner result than ad hoc placement, so
  prefer it over building the Excalidraw JSON by hand.
- **Neither found**: generate a valid Excalidraw scene file (`.excalidraw`,
  which is JSON) yourself and save it to the working directory. An Excalidraw
  scene is `{"type": "excalidraw", "version": 2, "elements": [...], "appState": {...}}`,
  where each element has at minimum `type` (`rectangle`, `text`, `arrow`,
  `ellipse`), `x`, `y`, `width`, `height`, and a unique `id`; arrows bind to
  shapes via `startBinding`/`endBinding` referencing element ids. Keep the
  same layered/grouped structure described above. Tell the user to open the
  file in Excalidraw via File → Open.

## Resources

- `references/architecture-checklist.md` — layer definitions, data-flow table
  template, collection-method decision guide, and security/networking
  checklist. Read this before Step 3.
