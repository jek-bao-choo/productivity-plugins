---
name: creating-solution-architecture
description: >-
  Design an end-to-end Datadog monitoring architecture diagram and render it
  in Excalidraw, from sales discovery notes and technical plans. Use when the
  user asks to "design a Datadog architecture diagram", "map out our
  monitoring architecture", "turn these discovery notes into an Excalidraw
  diagram", "draw the data flow for metrics/traces/logs", "show which ports
  and protocols the telemetry uses", "sketch how this customer's stack maps to
  Datadog", or wants a layered infra/app/UI blueprint showing collection
  methods (Agent, Cluster Agent, OpenTelemetry Collector, API integrations)
  and telemetry transmission (signal type, protocol, port) to the Datadog SaaS
  intake (EU/US/AP). Produces a current state view (fragmented monitoring
  tools) and a target state view (consolidated on Datadog), both flowing left
  to right from the customer environment to the destination. Outputs both
  an editable .excalidraw file and a .svg diagram. Also trigger
  this whenever the user provides discovery notes (markdown/Google Docs) or
  technical plans (CSV/Excel) and wants a visual architecture output,
  even if they don't say "Excalidraw" or "diagram" explicitly, or wants a current vs future state / tool
  consolidation picture — e.g. "help me plan how we'd monitor this customer's
  environment" or "what would the observability setup look like for this
  account".
version: "0.4.0"
---

# Create Datadog Architecture Diagram in Excalidraw

You are acting as a Senior Solutions Architect specializing in Cloud
Observability and Datadog implementations. Your job is to turn a prospect's
discovery notes and technical plans into a detailed, layered monitoring
architecture, and render it as a diagram in Excalidraw.

Every run delivers **two files** with the same content:

- `<customer>-architecture.excalidraw`: the editable source.
- `<customer>-architecture.svg`: a static diagram for slides, docs, email,
  and Slack, which open it without Excalidraw.

Use the customer's short name in lowercase with hyphens (e.g.
`acme-architecture.svg`), or `architecture` if there's no customer name.

The diagram must make **telemetry transmission explicit**: for every hop, a
reader should be able to see what kind of data moves (metrics, traces/spans,
logs, events, and which subtype), over which protocol, on which port, and in
which direction. This is what network and security teams review first, and a
diagram that just says "data → Datadog" can't be used to open firewall rules
or approve a design.

Every diagram tells a **current state → target state** story:

- **Current state**: the prospect's environment today, usually monitored by
  fragmented tooling (separate tools for metrics, logs, APM, alerting, often
  owned by different teams), with siloed data and no shared context.
- **Target state**: the same environment consolidated onto Datadog as one
  observability platform.

In both states, **telemetry flows left to right**: the customer or prospect
environment sits on the left, the monitoring tools (current state) or
Datadog (target state) sit on the right.

**Never draw a telemetry flow you can't stand behind.** An arrow on this
diagram is a claim that the data can actually be collected from that source
and delivered to its destination. If it's uncertain whether a source can be
instrumented, whether the data can leave the environment, or whether
Datadog supports it, don't draw the arrow. Call it out instead (see "Verify
every flow can actually happen" in Step 5). A diagram that shows telemetry
Datadog can't collect misleads the customer, sets up a failed PoC, and
costs credibility.

**Every word this skill generates is short, concise, and succinct.** That
covers diagram text, the transmission table, questions to the user, and the
final reply. See "Wording rules" below.

## Wording rules

A diagram is read at a glance on a shared screen. Long labels overlap
arrows, shrink to unreadable, and read as AI-generated.

**Defaults:**

- Fragments, not sentences. No filler ("in order to", "is responsible
  for", "leverages", "seamlessly").
- Use the customer's own names for systems and teams.
- Use `·` to separate parts of a label. Never use " — " or " - " as
  separators in generated text.
- Cut words rather than shrinking the font or wrapping past 2 lines.

**Word limits (hard caps):**

| Text | Limit | Example |
|---|---|---|
| Frame title | 5 words | `Current State: Fragmented Monitoring` |
| Node label | Name + 4 words, max 2 lines | `Checkout API · Java 17 · EKS` |
| Collection method tag | 3 words | `Datadog Agent`, `OTel Collector` |
| Current tool box | Tool · signal · owner | `Splunk · logs · SecOps` |
| Arrow label | Fixed format, 8 words | `Traces (APM spans) · HTTP/TCP · 8126` |
| Pain point callout | 6 words | `No trace ↔ log correlation` |
| Unverified / not possible callout | 5 words | `Unverified: Java 6 APM support` |
| "Not drawn" box row | 12 words | `Core banking · traces · Java 6 · Confirm: tracer support` |
| "What changes" callout | 3 bullets, 6 words each | `4 tools → 1 platform` |
| Legend entry | 2 words | `Traces/spans` |
| Table Notes cell | 8 words | `Proxy port from customer` |
| Question to the user | 1 sentence, 15 words | `Which Datadog site: US1, EU1, or AP1?` |

**Before / after:**

| Before | After |
|---|---|
| `The application sends trace data over HTTP to the local Datadog Agent on port 8126` | `Traces (APM spans) · HTTP/TCP · 8126` |
| `Telemetry path unverified because we don't know whether the Java 6 runtime is supported` | `Unverified: Java 6 APM support` |
| `Logs are currently collected by Splunk, which is owned by the security team` | `Splunk · logs · SecOps` |
| `There is currently no way to correlate traces with logs across tools` | `No trace ↔ log correlation` |

**Final reply to the user:** at most 5 bullets for the design summary, then
the "not drawn" list with one line per flow. No recap of the process.

## Workflow

Copy this checklist and tick it off as you go:

```
- [ ] Setup: check for Excalidraw MCP and an architecture skill
- [ ] Step 1: Analyze the inputs
- [ ] Step 2: Clarify before designing
- [ ] Step 3: Map the current state (fragmented tooling)
- [ ] Step 4: Design the target state blueprint (Datadog)
- [ ] Step 5: Build the telemetry transmission table
- [ ] Step 6: Render current state and target state in Excalidraw
- [ ] Step 6b: Export the .svg diagram and look at it
- [ ] Step 7: Final check (including wording limits)
```

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

What you find determines how you execute Step 6. Don't hard-code
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
- Existing monitoring/observability tools (e.g. Prometheus + Grafana,
  Splunk, ELK/OpenSearch, New Relic, Dynatrace, AppDynamics, Nagios/Zabbix,
  CloudWatch, PagerDuty/Opsgenie), what each one covers, which team owns it,
  and the pain points the notes mention (tool sprawl, no correlation, slow
  MTTR, cost, licence renewals)
- Which signals the customer cares about (metrics, traces, logs, events,
  alerts) and where alerts need to go (Slack, PagerDuty, ServiceNow, email,
  webhooks)
- Any stated compliance, data-residency, or security requirements
- Network topology hints: proxies, firewalls, PrivateLink, VPNs, blocked or
  custom ports
- Anything that could block collection: air-gapped or isolated networks,
  no outbound internet, restrictions on installing agents, unusual
  platforms (mainframe, AIX/Solaris, proprietary appliances, OT/SCADA),
  old or uncommon language runtimes, SaaS tools with no API or export

Don't force structure onto notes that don't have it yet — partial or messy
input is normal at this stage. The goal is just to surface what's known so
Step 2 can focus on what's actually missing.

## Step 2 — Clarify before designing

Guessing wrong here produces a plausible-looking diagram that's actually
wrong — e.g. assuming US region intake when the customer has an EU
data-residency requirement, or assuming Agent-based collection when the
environment is serverless-only. Before proposing the design, confirm anything
not already answered by the notes:

- Datadog site / intake region: US1, US3, US5, EU1, AP1, AP2, or US1-FED
- Compliance or data-residency constraints
- Preferred collection method per environment: Datadog Agent, Cluster Agent,
  OpenTelemetry Collector, or API-based integration
- How apps send traces: Datadog tracing libraries, or OpenTelemetry SDKs
  (OTLP gRPC vs OTLP HTTP)
- Network constraints: proxy, firewall egress rules, PrivateLink, and any
  ports that are blocked or must be changed from the defaults
- Alert destinations for monitor notifications
- For any source where collection is in doubt: can an agent or SDK be
  installed, which OS/runtime versions are involved, can the data leave the
  network, and does the system expose an API, log export, or syslog
- Current monitoring tools, if the notes don't name them (which tool covers
  metrics, logs, APM, alerting), and whether any of them stay in the target
  state (e.g. ServiceNow or PagerDuty kept as alert destinations)

Use `AskUserQuestion` if available; otherwise ask conversationally in your
response. Only ask about what the notes genuinely don't answer — if the
notes already say "EU region, GDPR compliance required," don't re-ask it.

If the collection method is unspecified and more than one would work, ask
rather than guess: the choice changes network requirements (Agent egress vs
Datadog polling the customer's cloud API) and should be a deliberate
decision.

## Step 3 — Map the current state (fragmented tooling)

Draw the prospect's environment as it is monitored today. The point of this
view is to make the fragmentation visible, so the target state reads as a
clear improvement:

- Use the **same customer environment nodes** (same Service Scope, same
  Infrastructure / Application / UI layers, same positions) on the left as
  in the target state, so the two views are directly comparable.
- On the right, draw **each existing tool as its own box**, labeled with
  what it covers and who owns it, e.g. "Prometheus + Grafana · metrics ·
  Platform team", "Splunk · logs · SecOps", "New Relic · APM · App team",
  "Nagios · uptime checks", "PagerDuty · alerting".
- Draw the arrows from each source to the tool that collects it, labeled
  with the signal, and with protocol and port where the notes give them
  (e.g. `Logs · Splunk UF/TCP · 9997`, `Metrics · Prometheus scrape/HTTP ·
  9100`). Don't invent ports the notes don't support; label the signal
  only and mark the protocol as "to confirm".
- Show the **gaps and silos**: no links between tools, duplicated agents on
  the same host, signals that aren't collected at all (e.g. no RUM, no
  traces for a legacy service), and manual correlation by people. Mark pain
  points from the notes with short callouts (e.g. "No trace ↔ log
  correlation", "3 agents per host", "Alert noise from 4 tools").

If the notes say nothing about existing tooling and the user confirms
there's nothing in place (greenfield), skip this view and say so, rather
than inventing tools.

## Step 4 — Design the target state blueprint (Datadog)

The target state consolidates the fragmented tools from Step 3 onto
Datadog as one platform. Map each current tool to the Datadog product that
replaces it (e.g. Prometheus + Grafana → Infrastructure Monitoring and
Dashboards, Splunk → Log Management, New Relic → APM, Nagios → Synthetics,
alert routing → Monitors and On-Call), and keep only the tools the customer
confirmed stay (usually ITSM or paging tools as alert destinations).

Organize the design by these dimensions.

### Service Scope

Which part of the customer's stack this covers. Group by environment
("Production", "Staging") or by business unit if the notes are organized
that way.

### Infrastructure Layer

The compute and platform substrate the workloads run on:

- Kubernetes clusters (EKS, GKE, AKS, OpenShift, self-managed)
- Virtual machines (EC2, Compute Engine, Azure VMs, on-prem)
- Serverless (Lambda, Cloud Functions, Azure Functions, Fargate)
- Managed data stores (RDS, managed Kafka, managed Redis) when the customer
  wants infra-level visibility into them

### Application Layer

The services and APIs that make up the customer's actual product:

- Microservices / monoliths and the APIs they expose
- Internal service-to-service calls (where distributed tracing matters most)
- Message queues / event buses connecting services
- Databases as accessed by the application (as opposed to DB host
  monitoring)

### UI/End-User Layer

Where the customer's own users interact with the product:

- Web/mobile frontends monitored via Real User Monitoring (RUM) and Session
  Replay
- Synthetic checks (API tests, browser tests) simulating user journeys,
  from managed locations or private locations
- CDN/edge layer if relevant to page load or delivery performance

### Collection method decision guide

Attach one of these to every node:

- **Datadog Agent** — default for VMs and bare-metal hosts where a
  long-running process can be installed. Also handles container workloads on
  a single host.
- **Datadog Cluster Agent** — for Kubernetes, alongside the node Agent
  DaemonSet, when the customer wants cluster-level metadata, cluster checks,
  the admission controller (auto-injection of tracers), or external metrics
  for HPA.
- **OpenTelemetry Collector** — when the customer already has OTel
  instrumentation, wants a vendor-neutral collection layer, or needs to fan
  out telemetry to multiple backends. Forwards to Datadog via the Datadog
  exporter or an OTLP endpoint (Datadog Agent OTLP ingest or Datadog OTLP
  intake).
- **API-based integration** — for SaaS/managed services with no host to
  install an agent on (cloud provider integrations, third-party SaaS).
  Datadog pulls the data, so there's no agent footprint and no customer
  egress, but it needs credentials (IAM role, service principal, API key).
- **Serverless** — Datadog Lambda Extension / serverless libraries, or the
  Datadog Forwarder for CloudWatch logs.
- **Browser / mobile SDK** — RUM SDK in the frontend, sending straight from
  the end user's device.

### Security & networking overlay

Check the notes for each of these (and ask about anything missing):

- **Proxy** — if telemetry routes through an outbound proxy, draw it as an
  explicit node between the collection layer and Datadog intake, with its
  listen port (e.g. Squid on TCP 3128, HAProxy on a custom port).
- **Firewall rules** — list the Datadog domains and ports that egress
  rules must allow. Domains depend on the confirmed site (e.g.
  `*.datadoghq.com`, `*.datadoghq.eu`, `*.ap1.datadoghq.com`), so use the
  region confirmed in Step 2 instead of assuming one.
- **PrivateLink** — if the customer uses AWS PrivateLink (or Azure Private
  Link / GCP Private Service Connect) to avoid public internet egress, draw
  the VPC endpoint between the customer's VPC and Datadog intake rather than
  a direct arrow. PrivateLink is available for specific sites and regions
  only, so confirm it fits the chosen site.

Draw these as their own overlay rather than folding them into the data-flow
arrows, so a reviewer can see the security posture at a glance.

## Step 5 — Build the telemetry transmission table

This is the core of the design. Break telemetry down **per signal and per
hop**, never as one generic "telemetry" arrow. Metrics, traces, and logs
often take different paths even from the same source (e.g. logs are tailed
from files by the Agent while traces are pushed by the app to the Agent over
HTTP), so one arrow per source is not enough.

### Signal taxonomy

Classify every flow into one of these signals and name the subtype:

| Signal | Subtypes to name explicitly |
|---|---|
| **Metrics** | Infrastructure/host metrics, integration metrics, custom metrics (DogStatsD/OTLP), Kubernetes state metrics, cloud metrics (CloudWatch/Azure Monitor/GCP), APM trace metrics, RUM metrics |
| **Traces / spans** | APM traces made of spans (Datadog tracer or OTLP spans), profiles if Continuous Profiler is in scope |
| **Logs** | Application logs, container stdout/stderr, system/syslog, audit logs, cloud service logs (CloudTrail, VPC flow logs) |
| **Events** | Alert events (monitor notifications), Kubernetes events, integration events, deployment/change events, custom events (API or DogStatsD), security signals |
| **Other** | Service checks, process/container data, network performance data, RUM sessions and Session Replay, Synthetics results, Remote Configuration |

Be explicit about direction for events too: **alert events** are generated
inside Datadog and flow *outbound from Datadog* to notification channels,
which is the opposite direction from collected telemetry. Show them as a
separate arrow out of the Datadog box.

### Default protocols and ports

Use these defaults unless the notes say otherwise. If the customer has
changed a port, use theirs and note it.

**Inside the customer environment (app → Agent / Collector):**

| Flow | Signal | Protocol | Port |
|---|---|---|---|
| App → Agent DogStatsD | Custom metrics, events, service checks | UDP (or Unix domain socket) | 8125 |
| App tracer → Agent trace intake | Traces/spans, profiles | HTTP over TCP (or Unix domain socket) | 8126 |
| App OTel SDK → Agent or OTel Collector | Metrics, traces, logs | OTLP/gRPC | 4317 |
| App OTel SDK → Agent or OTel Collector | Metrics, traces, logs | OTLP/HTTP | 4318 |
| Agent tails log files / container runtime | Logs | Local file or container socket read | n/a |
| Network devices → Agent syslog listener | Logs | Syslog over TCP/UDP | Customer-defined (e.g. 514) |
| Node Agent → Cluster Agent | Cluster metadata, cluster checks | HTTPS over TCP | 5005 |
| Kubernetes API server → Cluster Agent | Admission controller webhook | HTTPS | 8000 (Service port 443) |
| Kubernetes HPA → Cluster Agent | External metrics | HTTPS | 8443 |
| Agent → monitored database | Database Monitoring queries | DB native protocol | DB port (e.g. 5432 Postgres, 3306 MySQL) |

**Leaving the customer environment (to Datadog intake):**

| Flow | Signal | Protocol | Port |
|---|---|---|---|
| Agent → Datadog metrics intake | Metrics, service checks, events, process data | HTTPS over TCP | 443 |
| Agent → Datadog trace intake | Traces/spans, profiles | HTTPS over TCP | 443 |
| Agent → Datadog logs intake | Logs | HTTPS over TCP (default) | 443 |
| Agent → Datadog logs intake (legacy TCP mode) | Logs | TCP with TLS | 10516 (US1), 443 for some other sites |
| OTel Collector (Datadog exporter) → Datadog | Metrics, traces, logs | HTTPS over TCP | 443 |
| Lambda Extension / Forwarder → Datadog | Metrics, traces, logs | HTTPS over TCP | 443 |
| Browser / mobile RUM SDK → Datadog | RUM events, Session Replay, browser logs | HTTPS over TCP | 443 |
| Synthetics private location → Datadog | Test config and results | HTTPS over TCP | 443 |
| Agent → Datadog Remote Configuration | Config and tracer settings | HTTPS over TCP | 443 |
| Agent → NTP servers (optional) | Clock sync | NTP over UDP | 123 |

**Initiated by Datadog:**

| Flow | Signal | Protocol | Port |
|---|---|---|---|
| Datadog → cloud provider APIs (CloudWatch, Azure Monitor, GCP) | Cloud metrics, logs, resource metadata | HTTPS (Datadog polls) | 443 |
| Datadog → notification channels (Slack, PagerDuty, email, webhooks) | Alert events from monitors | HTTPS (or SMTP for email) | 443 |
| Datadog managed Synthetics locations → customer endpoints | Synthetic test traffic | HTTP(S), TCP, DNS, ICMP, etc. | Whatever the tested endpoint listens on |

When PrivateLink is used, the outbound HTTPS 443 flows go to the VPC
endpoint instead of the public intake, so label them that way. When a proxy
is used, split each outbound flow into two hops (Agent → proxy on the
proxy's port, proxy → Datadog on 443).

If you're unsure whether a port or endpoint applies to the customer's site
or Agent version, say so in the notes column and recommend confirming
against the Datadog "Network Traffic" docs for that site, rather than
stating it as fact.

### Verify every flow can actually happen

Before a row goes into the table as drawable, check it end to end. Give
every flow one of three statuses:

| Status | Meaning | On the diagram |
|---|---|---|
| **Confirmed** | The notes or the user confirm the source can be instrumented (agent/SDK can be installed, or an API/export exists), the platform and version are supported by the chosen collection method, and the network path to the destination is open (direct, proxy, or PrivateLink). | Draw the arrow with its full label. |
| **Unverified** | Any link in that chain is unknown or assumed: unsupported or unknown OS/runtime version, unclear whether agents can be installed, unknown egress, no known API or log export, a Datadog product or PrivateLink whose availability for the chosen site isn't confirmed, or a port you're guessing. | **Do not draw the arrow.** Draw the source node with a "Telemetry path unverified" callout stating what's unknown, and list it in the "Not drawn: needs confirmation" box. |
| **Not possible** | Collection is known to be blocked: air-gapped with no allowed egress and no relay, agents forbidden and no API/export, a platform the collection method doesn't support, or the customer has ruled it out. | **Do not draw the arrow.** Draw the source node with a "No telemetry path" callout and the reason, and list it in the "Not drawn" box. |

Rules that apply in every case:

- **Uncertainty means no arrow.** Don't draw a dashed, grey, or "maybe"
  arrow as a compromise. A reader will still take any line as a working
  path. The only dashed arrow allowed is Synthetic test traffic, which is a
  real flow.
- **Check every hop, not just the last one.** A flow is only Confirmed if
  every hop is (source → agent/collector → proxy/PrivateLink → Datadog). If
  the app → Agent hop is fine but the egress is unknown, the whole flow is
  Unverified.
- **Check every signal separately.** A host can have Confirmed metrics and
  logs while traces are Unverified because the runtime isn't supported by a
  tracer. Draw the confirmed arrows and call out the rest.
- **Don't fill gaps from general knowledge alone.** If you believe something
  is supported but the notes don't confirm the version, platform, or
  network path, mark it Unverified and say what to check (e.g. `Confirm:
  Java 6 tracer support`, `Confirm: appliance syslog forwarding`, `Confirm:
  OT network egress`).
- **Same rule for the current state.** Only draw arrows from a source to an
  existing tool when the notes say that tool collects it. Don't assume
  coverage. Because those flows exist today, a missing protocol or port can
  be labeled "to confirm" instead of hiding the arrow.

Raise every Unverified item with the user (Step 2 style questions) before
finalizing if you can. Whatever is still open goes in the callouts and the
"Not drawn" box, never as an arrow.

### Table template

Fill one row per signal per hop. This table goes in the blueprint and drives
every arrow in the diagram:

| Source | Destination | Signal | Subtype | Protocol | Port | Direction | Collection method | Site / endpoint | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Checkout service (EKS pod) | Node Agent | Traces/spans | APM spans from dd-trace-java | HTTP over TCP | 8126 | Pod → Agent | Datadog tracer | — | Confirmed | Admission controller injects tracer |
| Checkout service (EKS pod) | Node Agent | Metrics | Custom business metrics | DogStatsD over UDP | 8125 | Pod → Agent | DogStatsD client | — | Confirmed | — |
| EKS node | Node Agent | Logs | Container stdout/stderr | Local container log read | n/a | Node → Agent | Agent log collection | — | Confirmed | — |
| Node Agent | Datadog | Metrics, traces, logs | All of the above | HTTPS over TCP | 443 | Customer → Datadog | Datadog Agent | AP1 via PrivateLink endpoint | Confirmed | — |
| Legacy VM | Proxy | Logs | App + syslog | HTTPS over TCP | 3128 | VM → proxy | Datadog Agent | — | Confirmed | Proxy listen port from customer |
| Proxy | Datadog | Logs | App + syslog | HTTPS over TCP | 443 | Customer → Datadog | — | EU1 logs intake | Confirmed | — |
| AWS account | Datadog | Metrics | CloudWatch metrics | HTTPS (pull) | 443 | Datadog → AWS API | AWS integration (IAM role) | US1 | Confirmed | No customer egress |
| React web app | Datadog | Other | RUM sessions, Session Replay | HTTPS over TCP | 443 | Browser → Datadog | RUM Browser SDK | EU1 browser intake | Confirmed | — |
| Datadog monitors | PagerDuty, Slack | Events | Alert events | HTTPS | 443 | Datadog → SaaS | Monitor notifications | — | Confirmed | Outbound from Datadog |
| Core banking (AIX, Java 6) | Datadog | Traces/spans | APM spans | — | — | — | Unknown | — | Unverified | Java 6 APM support unknown |
| OT network PLCs | Datadog | Metrics | Device metrics | — | — | — | None | — | Not possible | Air-gapped, no egress |

The examples above are illustrative. Replace them with the customer's actual
sources, signals, and ports. Only **Confirmed** rows become arrows.

## Step 6 — Render in Excalidraw

### Two views: current state and target state

Produce two views on the same canvas, each in its own labeled Excalidraw
frame: **"Current State: Fragmented Monitoring"** on top and **"Target
State: Consolidated on Datadog"** below it. Use the same width and the same
positions for the customer environment nodes in both, so a reader can look
straight down from one to the other. Optionally add a short "What changes"
callout between them (e.g. `4 tools → 1 platform`, `1 Agent per host`,
`Traces, logs, metrics correlated`).

### Left-to-right layout (both views)

Telemetry always flows **left to right**, in columns:

1. **Left: customer / prospect environment.** Group nodes by **Service
   Scope**, and inside each scope stack the **UI, Application, and
   Infrastructure** layers as horizontal swimlanes (top to bottom), so
   every lane can send its arrows to the right.
2. **Middle: collection and network edge.** Agents, Cluster Agent, OTel
   Collector (target state) or each tool's own agents and forwarders
   (current state), followed by proxy, firewall, and PrivateLink endpoint
   nodes at the customer boundary. Draw the customer boundary as a dashed
   rectangle around the left and middle columns.
3. **Right: destination.** In the current state, the separate monitoring
   tools stacked vertically. In the target state, a single **Datadog SaaS**
   box labeled with the site (e.g. "Datadog EU1 · datadoghq.eu"), with the
   Datadog products inside it (Infrastructure, APM, Log Management, RUM,
   Synthetics, Monitors, etc.).
4. **Far right: notification channels** (Slack, PagerDuty, ServiceNow,
   email), so alert events keep flowing left to right out of Datadog (or
   out of the current alerting tool).
5. Annotate each node with its collection method so the diagram doubles as
   an implementation checklist.

### Telemetry arrows

Every **Confirmed** row of the transmission table becomes an arrow.
Unverified and Not possible rows never become arrows. Each arrow:

- **Is colored by signal type**, consistently across the diagram, for
  example: metrics = blue, traces/spans = purple, logs = green, events =
  orange, alert events = red, other (RUM, Synthetics, Remote Config) = grey.
- **Carries a label in this format:** `<Signal> (<subtype>) · <protocol> ·
  <port>`, e.g. `Traces (APM spans) · HTTP/TCP · 8126`,
  `Metrics (custom) · DogStatsD/UDP · 8125`,
  `Logs · HTTPS/TCP · 443 → EU1`, `Alert events · HTTPS · 443`.
- **Points left to right, in the direction the data travels**, from the
  customer environment toward Datadog, and from Datadog toward
  notification channels. For pull-based flows (cloud API integrations,
  Prometheus scrapes) keep the arrow pointing left to right and add
  "(pulled by Datadog)" or "(scraped)" to the label, so the direction of
  the connection is still clear without breaking the flow. The one
  exception is Datadog managed Synthetics locations testing customer
  endpoints: draw it as a dashed arrow from right to left and label it
  "Synthetic test traffic".
- Is split per hop when it passes through a proxy, OTel Collector, or
  PrivateLink endpoint, with the right port on each hop.

If several signals share exactly the same hop, protocol, and port (e.g.
Agent → Datadog on 443), you can merge them into one arrow, but list every
signal in the label (`Metrics + Traces + Logs · HTTPS/TCP · 443`).

Add a **"Not drawn: needs confirmation"** box in each view, listing every
Unverified or Not possible flow with its source, signal, reason, and what
needs to be confirmed. Mark the matching source nodes with a short callout
(`Unverified: runtime support` or `No path: air-gapped`) so nobody reads the missing arrow as an oversight.

Add a **legend** box explaining the colors, and a **ports summary** box
listing every port a firewall team needs to open (source, destination,
protocol, port), grouped into "inside the cluster/host" and "egress to
Datadog".

### Rendering path

Pick the path based on what Setup found:

- **Excalidraw MCP tool found**: call it directly to build the diagram with
  the layout and arrow rules above.
- **Architecture skill found**: invoke it (via the `Skill` tool) to handle
  the diagram-construction mechanics, since it may have layout or shape
  conventions that produce a cleaner result than ad hoc placement. Pass it
  the transmission table and the arrow rules above so the signal, protocol,
  and port labels are kept.
- **Neither found**: generate a valid Excalidraw scene file (`.excalidraw`,
  which is JSON) yourself and save it to the working directory as
  `<customer>-architecture.excalidraw`. A scene is
  `{"type": "excalidraw", "version": 2, "elements": [...], "appState": {...}}`,
  where each element has at minimum `type` (`rectangle`, `text`, `arrow`,
  `ellipse`), `x`, `y`, `width`, `height`, and a unique `id`. Arrows bind
  to shapes via `startBinding`/`endBinding` referencing element ids, set
  their color with `strokeColor`, and get a label via a bound `text`
  element (`containerId` set to the arrow's id, and the arrow listing it in
  `boundElements`). Use two `frame` elements for the current state and
  target state views, and set `frameId` on each element to the frame it
  belongs to. Tell the user to open the file in Excalidraw via
  File → Open.

Whatever path you took, end Step 6 with `<customer>-architecture.excalidraw`
saved in the working directory. If the MCP tool or architecture skill
built the diagram, export or fetch the scene JSON from it. If it can't give
you the JSON, write the same scene yourself from the transmission table and
layout so both files match.

## Step 6b — Export the .svg diagram

If the MCP tool or architecture skill can export SVG directly, use that and
save it as `<customer>-architecture.svg`. Otherwise convert the scene file
with this script. It draws rectangles, ellipses, diamonds, frames (with
their names), arrows and lines (with colors, dashes, and arrowheads), and
text, including labels bound to shapes and arrows:

```bash
python3 -I - acme-architecture.excalidraw acme-architecture.svg <<'PY'
import json, sys, html
src, out = sys.argv[1], sys.argv[2]
els = [e for e in json.load(open(src))["elements"] if not e.get("isDeleted")]
byid = {e["id"]: e for e in els}
FONT = "Helvetica, Arial, sans-serif"
xs, ys = [], []
for e in els:
    x, y, w, h = e.get("x", 0), e.get("y", 0), e.get("width", 0), e.get("height", 0)
    pts = e.get("points") or [[0, 0], [w, h]]
    xs += [x + p[0] for p in pts] + [x, x + w]
    ys += [y + p[1] for p in pts] + [y, y + h]
pad = 40
minx, miny = min(xs) - pad, min(ys) - pad
W, H = max(xs) - minx + pad, max(ys) - miny + pad
def attrs(e, fill=True):
    a = f'stroke="{e.get("strokeColor", "#1e1e1e")}" stroke-width="{e.get("strokeWidth", 1.5)}"'
    bg = e.get("backgroundColor", "transparent")
    a += f' fill="{bg if fill and bg != "transparent" else "none"}"'
    if e.get("strokeStyle") == "dashed": a += ' stroke-dasharray="8 6"'
    if e.get("strokeStyle") == "dotted": a += ' stroke-dasharray="2 4"'
    return a
def text(x, y, t, size, color, anchor="middle", weight="normal"):
    lines = t.split("\n")
    y0 = y - (len(lines) - 1) * size * 0.6
    spans = "".join(f'<tspan x="{x:.1f}" y="{y0 + i * size * 1.2:.1f}">{html.escape(l)}</tspan>' for i, l in enumerate(lines))
    return (f'<text font-family="{FONT}" font-size="{size}" fill="{color}" text-anchor="{anchor}" '
            f'dominant-baseline="middle" font-weight="{weight}">{spans}</text>')
shapes, labels = [], []
for e in els:
    t, x, y = e["type"], e.get("x", 0), e.get("y", 0)
    w, h = e.get("width", 0), e.get("height", 0)
    if t in ("rectangle", "frame"):
        r = 8 if e.get("roundness") else 0
        a = attrs(e) if t == "rectangle" else 'stroke="#9e9e9e" stroke-width="1.5" fill="none" stroke-dasharray="4 4"'
        shapes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" {a}/>')
        if t == "frame" and e.get("name"):
            labels.append(text(x, y - 14, e["name"], 20, "#1e1e1e", "start", "bold"))
    elif t == "ellipse":
        shapes.append(f'<ellipse cx="{x + w/2}" cy="{y + h/2}" rx="{w/2}" ry="{h/2}" {attrs(e)}/>')
    elif t == "diamond":
        shapes.append(f'<polygon points="{x+w/2},{y} {x+w},{y+h/2} {x+w/2},{y+h} {x},{y+h/2}" {attrs(e)}/>')
    elif t in ("arrow", "line"):
        pts = " ".join(f"{x + p[0]},{y + p[1]}" for p in e.get("points", [[0, 0], [w, h]]))
        c = e.get("strokeColor", "#1e1e1e")
        m = ""
        if t == "arrow" and e.get("endArrowhead", "arrow"):
            mid = "m" + c.lstrip("#")
            shapes.append(f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" '
                          f'markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker></defs>')
            m = f' marker-end="url(#{mid})"'
            if e.get("startArrowhead"): m += f' marker-start="url(#{mid})"'
        shapes.append(f'<polyline points="{pts}" {attrs(e, fill=False)}{m}/>')
    elif t == "text":
        size, color = e.get("fontSize", 16), e.get("strokeColor", "#1e1e1e")
        c = byid.get(e.get("containerId") or "")
        if c and c["type"] in ("arrow", "line"):
            p = c.get("points", [[0, 0]]); a, b = p[len(p)//2 - 1] if len(p) > 1 else p[0], p[len(p)//2]
            cx, cy = c["x"] + (a[0] + b[0]) / 2, c["y"] + (a[1] + b[1]) / 2
            n = max(len(l) for l in e["text"].split("\n")) * size * 0.55
            k = len(e["text"].split("\n")) * size * 1.2
            labels.append(f'<rect x="{cx - n/2 - 4}" y="{cy - k/2 - 2}" width="{n + 8}" height="{k + 4}" fill="#ffffff"/>')
            labels.append(text(cx, cy, e["text"], size, color))
        elif c:
            labels.append(text(c["x"] + c["width"] / 2, c["y"] + c["height"] / 2, e["text"], size, color))
        else:
            anchor = {"left": "start", "right": "end"}.get(e.get("textAlign", "left"), "middle")
            tx = x if anchor == "start" else x + w if anchor == "end" else x + w / 2
            labels.append(text(tx, y + h / 2, e["text"], size, color, anchor))
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{minx} {miny} {W} {H}" width="{W}" height="{H}">'
       f'<rect x="{minx}" y="{miny}" width="{W}" height="{H}" fill="#ffffff"/>' + "".join(shapes + labels) + "</svg>")
open(out, "w").write(svg)
print(f"wrote {out} ({len(els)} elements)")
PY
```

Then check the SVG:

1. **It parses:** `python3 -I -c "import xml.dom.minidom as m; m.parse('acme-architecture.svg'); print('valid')"`
2. **It looks right:** render it to PNG and open the image with `Read`.
   Prefer headless Chrome, since it renders SVG faithfully:
   `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --screenshot=preview.png --window-size=1800,1400 file://$PWD/acme-architecture.svg`.
   If Chrome isn't available, use `qlmanage -t -s 1800 -o . acme-architecture.svg`
   (macOS; its thumbnail may crop, so don't treat cropping as a bug).
3. **Fix what you see:** overlapping labels, text spilling out of boxes,
   arrows crossing nodes, or arrows that don't run left to right. Fix the
   `.excalidraw` scene, not the SVG, then convert again so both files stay
   in sync.

Delete `preview.png` when you're done; deliver only the two diagram files.

## Step 7 — Final check

Before handing over, confirm:

- Both views are present (current state on top, target state below),
  unless the user confirmed a greenfield environment.
- Telemetry flows left to right in both views: customer environment on the
  left, tools or Datadog on the right, notification channels on the far
  right.
- The customer environment nodes are in the same positions in both views.
- The current state shows each existing tool separately with its coverage
  and owner, plus the silos and pain points from the notes, and no tools
  that the notes don't mention.
- Every current tool is mapped to the Datadog product that replaces it, or
  kept on purpose as confirmed by the user.
- Every source in the notes appears as a node with a collection method.
- Every arrow on the diagram is a **Confirmed** flow, checked on every hop.
  There are no arrows for Unverified or Not possible flows, in either view.
- Every Unverified or Not possible flow has a callout on its source node and
  a line in the "Not drawn: needs confirmation" box saying what to confirm.
- Every node that emits telemetry has an arrow for **each** signal it sends,
  not one generic arrow.
- Every arrow label states signal (and subtype), protocol, and port.
- Alert events are shown flowing out of Datadog to the notification
  channels.
- Proxy, firewall, and PrivateLink are drawn as explicit nodes where they
  apply, and outbound hops through them carry the right ports.
- The Datadog site/region on the diagram matches what was confirmed in
  Step 2.
- The legend and ports summary are present.
- Both `<customer>-architecture.excalidraw` and `<customer>-architecture.svg`
  exist, the SVG parses, you've looked at a render of it, and it matches
  the scene.
- Every piece of text meets the word limits in "Wording rules", with no
  " — " or " - " separators. If you wrote a `.excalidraw` file, run this
  check and shorten anything it flags (use the cap from the table when it
  is tighter than 12):

  ```bash
  python3 -I - acme-architecture.excalidraw <<'PY'
  import json, sys
  els = json.load(open(sys.argv[1]))["elements"]
  bad = 0
  for e in els:
      t = e.get("text", "") if e.get("type") == "text" else ""
      for line in t.splitlines():
          if len(line.split()) > 12 or " — " in line or " - " in line:
              print("SHORTEN:", line); bad += 1
      if len(t.splitlines()) > 3:
          print("TOO MANY LINES:", t.replace("\n", " / ")); bad += 1
  print("OK" if not bad else f"{bad} issue(s)")
  PY
  ```

  If you used the Excalidraw MCP or an architecture skill instead, apply
  the same check to the text you sent.

Then share both file paths and the transmission table alongside the diagram, so the customer's
network team can review it as text as well. In your reply, list the flows
you didn't draw and why (one short line each), so the user knows what to
confirm with the customer before the diagram is shown as a commitment.
