---
name: creating-solution-architecture
description: >-
  Design an end-to-end Datadog monitoring architecture diagram from sales
  discovery notes and technical plans, drawn with Claude Artifact Design
  (fallback: a hybrid HTML file to drop into Claude Artifact Design). Use when the user asks to "design a Datadog
  architecture diagram", "map out our monitoring architecture", "turn these
  discovery notes into an architecture diagram", "draw the data flow for
  metrics/traces/logs", "show which ports and protocols the telemetry uses",
  or wants a layered infra/app/UI blueprint with collection methods (Agent,
  Cluster Agent, OTel Collector, API integrations) and per signal protocol
  and port to the Datadog intake (EU/US/AP). Draws a current state
  (fragmented tools) and a target state (consolidated on Datadog), left to
  right. Also trigger when the user shares discovery notes or technical
  plans and wants a visual architecture or current vs future state picture,
  e.g. "help me plan how we'd monitor this customer's environment".
version: "0.8.0"
---

# Create Datadog Architecture Diagram

You are acting as a Senior Solutions Architect specializing in Cloud
Observability and Datadog implementations. Your job is to turn a prospect's
discovery notes and technical plans into a detailed, layered monitoring
architecture, and draw it as a diagram.

**Draw the diagram with Claude Artifact Design. This is the top
preference.** Only when Claude Artifacts are not available or accessible,
write a hybrid HTML file instead (HTML and CSS boxes, inline SVG arrows).
The user then drops that HTML into Claude Artifact Design, so build it for
that hand-off. Never use Excalidraw.

Every run delivers:

- **Claude Artifact Design available**: a Claude Artifact holding the
  diagram, plus `<customer>-architecture.svg` (or `.png`) exported from it
  when the Artifact can export (for slides, docs, email and Slack).
- **Not available**: `<customer>-architecture.html` (to drop into Claude
  Artifact Design) and `<customer>-architecture.png`, a render of it for
  slides, docs, email and Slack.

Use the customer's short name in lowercase with hyphens (e.g.
`acme-architecture.html`), or `architecture` if there's no customer name.

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
- [ ] Setup: check for Claude Artifact Design
- [ ] Step 1: Analyze the inputs
- [ ] Step 2: Clarify before designing
- [ ] Step 3: Map the current state (fragmented tooling)
- [ ] Step 4: Design the target state blueprint (Datadog)
- [ ] Step 5: Build the telemetry transmission table
- [ ] Step 6: Draw both views (Artifact Design, else hybrid HTML)
- [ ] Step 6b: Look at the rendered diagram and fix it
- [ ] Step 7: Final check (including wording limits)
```

## Setup: check for Claude Artifact Design

Before Step 1, find out which drawing path this run can use:

- Check your tools for Claude Artifacts (e.g. an `Artifact` tool). If none
  is listed, run `ToolSearch` with `"artifact"` and then `"design"`.
- Claude Artifact Design is available when you can create an Artifact with
  its Design capability (Claude Design now lives in Claude).
- `DesignSync` is not a drawing tool. It only syncs design-system projects,
  so don't use it here.

Record the result: **Artifact path** or **HTML path**. Don't call a tool you
haven't confirmed exists; fall back to the HTML path instead. If the
Artifact path fails mid-run, say so in one line and switch to the HTML path.

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

## Step 6 — Draw the diagram

### Two views: current state and target state

Produce two views on the same canvas, each in its own labeled
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

Pick the path recorded in Setup.

**Artifact path (preferred).** Build the diagram as one Claude Artifact
using Claude Artifact Design:

- Give it the transmission table, the layout, the arrow rules, the colors
  and the wording rules above. They are the spec; Design styles the look.
- One canvas, two labeled frames: current state on top, target state below.
- Keep every label as real text, not baked into an image, so it stays
  editable.
- Use the Artifact's Datadog styles for fonts and colors where it has them,
  but keep the per signal arrow colors and the legend.
- If the Artifact can export SVG (or PNG), save it as
  `<customer>-architecture.svg` (or `.png`) in the working directory.
  Otherwise say so; the Artifact is the deliverable.

**HTML path (fallback).** Write `<customer>-architecture.html` in the
working directory, ready for the user to drop into Claude Artifact Design.
Boxes and labels are HTML and CSS, so Design can edit and restyle them;
arrows are inline SVG, so they stay exact.

- One self-contained file: inline `<style>`, no JavaScript, no external
  files. Font: Roboto, falling back to Helvetica, Arial, sans-serif.
- Plan the grid first (column x positions, lane y positions, node size) so
  boxes and labels don't collide and both views line up.
- One `<section class="view" id="current-state">` and one
  `id="target-state"`, each `position: relative` with a fixed size (about
  2400 × 900 px) and an `<h2>` title. Give both the same size and the same
  node positions on the left.
- Every node is a `<div class="node" id="...">` placed with
  `position: absolute` and explicit `left`, `top`, `width`, `height` in px,
  text centered, a `<br>` for the second line. Use classes for kinds
  (`node tool`, `node datadog`, `node proxy`, `callout`, `not-drawn`,
  `legend`, `ports`) so styling lives in the CSS. The customer boundary is a
  `div` with a dashed border.
- Arrows go on one `<svg class="flows">` per view: `position: absolute;
  inset: 0`, same size as the view, `pointer-events: none`, on top of the
  nodes. Each arrow is a `<path>` from the right edge of its source box to
  the left edge of its target box (use the px values you placed the boxes
  at), with `marker-end` and one `<marker>` per signal color in `<defs>`.
  Set `data-signal` (`metrics`, `traces`, `logs`, `events`, `alerts`,
  `other`) on each path. Put each arrow label as `<text>` at the midpoint on
  a white `<rect>` so it stays readable over lines. Size the rect to the
  text: about 0.6 × font size per character, plus 12 px.
- The legend, ports summary and "Not drawn" box are HTML (`<table>` for the
  ports summary).
- Add a comment at the top of each view and each flow group
  (`<!-- Target state · Agent egress -->`) so Design can map it.
- In your reply, tell the user: open Claude, drop in
  `<customer>-architecture.html`, and ask Claude Artifact Design to turn it
  into the diagram.

## Step 6b — Look at the diagram and fix it

1. **Artifact path:** open the rendered Artifact and look at both views.
   **HTML path:** render it with headless Chrome and open the image with
   `Read`:
   `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --hide-scrollbars --screenshot=acme-architecture.png --window-size=2400,1900 file://$PWD/acme-architecture.html`.
   Set the window height to fit both views.
2. **Fix what you see:** overlapping labels, text spilling out of boxes,
   arrows that miss their boxes or cross nodes, or arrows that don't run
   left to right. Fix the Artifact or the HTML, then look again. On the HTML
   path, re-take the screenshot after each fix; the last one is the `.png`
   deliverable.

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
- The diagram was drawn with Claude Artifact Design, or, only if Claude
  Artifacts weren't available, as a hybrid `.html` plus its `.png` render.
  No Excalidraw. You've looked at the render and fixed what you saw.
- Every piece of text meets the word limits in "Wording rules", with no
  " — " or " - " separators. On the HTML path, run this check and shorten
  anything it flags (use the cap from the table when it is tighter than
  12). On the Artifact path, apply the same check to the text you put in
  the Artifact:

  ```bash
  python3 -I - acme-architecture.html <<'PY'
  import sys, re, html
  doc = open(sys.argv[1]).read()
  doc = re.sub(r"(?s)<(style|defs)\b.*?</\1>|<!--.*?-->", "", doc)
  bad = 0
  for block in re.findall(r"(?s)>([^<>]*(?:<br\s*/?>[^<>]*)*)<", doc):
      lines = [html.unescape(l).strip() for l in re.split(r"<br\s*/?>", block)]
      lines = [l for l in lines if l]
      for line in lines:
          if len(line.split()) > 12 or " — " in line or " - " in line:
              print("SHORTEN:", line); bad += 1
      if len(lines) > 3:
          print("TOO MANY LINES:", " / ".join(lines)); bad += 1
  print("OK" if not bad else f"{bad} issue(s)")
  PY
  ```

Then share the Artifact (or the `.html` and `.png` paths) and the transmission table alongside the diagram, so the customer's
network team can review it as text as well. In your reply, list the flows
you didn't draw and why (one short line each), so the user knows what to
confirm with the customer before the diagram is shown as a commitment.
