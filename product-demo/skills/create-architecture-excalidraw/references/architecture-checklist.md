# Architecture Design Checklist

Reference for building the layered blueprint in Step 3 of the skill. Use this
to structure the design before rendering it in Excalidraw — don't skip
straight to drawing without first working through the layers, data flow, and
collection methods below.

## Layers

### Infrastructure Layer
The compute and platform substrate the customer's workloads run on. Typical
components:
- Kubernetes clusters (EKS, GKE, AKS, self-managed)
- Virtual machines (EC2, Compute Engine, Azure VMs, on-prem)
- Serverless (Lambda, Cloud Functions, Azure Functions)
- Managed data stores (RDS, managed Kafka, managed Redis) if the customer
  wants infra-level visibility into them

### Application Layer
The services and APIs that make up the customer's actual product:
- Microservices / monoliths and the APIs they expose
- Internal service-to-service calls (this is where distributed tracing
  matters most)
- Message queues / event buses connecting services
- Databases as accessed by the application (as opposed to infra-level DB
  host monitoring)

### UI/End-User Layer
Where the customer's own users interact with the product:
- Web/mobile frontends monitored via Real User Monitoring (RUM)
- Synthetic checks (API tests, browser tests) simulating user journeys
- CDN/edge layer if relevant to page load or delivery performance

## Data flow table template

For each source, map out how its telemetry reaches Datadog. Fill this in
during Step 3 and use it directly as the basis for the arrows in the diagram:

| Source | Telemetry Type | Collection Method | Destination Region | Notes |
|---|---|---|---|---|
| e.g. EKS cluster (prod) | Metrics, Logs | Datadog Cluster Agent | EU | via PrivateLink |
| e.g. Payment API service | Traces | OpenTelemetry Collector → Datadog Agent | EU | mTLS to collector |
| e.g. Legacy VM fleet | Metrics, Logs | Datadog Agent (host-installed) | EU | egress via proxy |
| e.g. Third-party SaaS billing | Metrics | API-based integration | US | no agent, pull-based |
| e.g. React web app | RUM, Session Replay | Browser SDK (RUM) | EU | — |
| e.g. Critical user flows | Synthetic checks | Synthetics API tests | EU | — |

Metrics, Traces, and Logs often take different paths even from the same
source (e.g. logs go straight to intake while traces route through an
OTel Collector first) — don't assume one arrow per source covers all three.

## Collection method decision guide

Use this to decide what to put in the "Collection Method" column above:

- **Datadog Agent** — default for VMs and bare-metal hosts where you can
  install a long-running process. Also handles container workloads on a
  single host.
- **Datadog Cluster Agent** — for Kubernetes specifically, when the customer
  wants cluster-level metadata (cluster checks, admission controller,
  external metrics) rather than just per-node agents.
- **OpenTelemetry Collector** — when the customer already has OTel
  instrumentation, wants a vendor-neutral collection layer, or needs to
  fan out telemetry to multiple backends. Can forward to Datadog via the
  Datadog exporter or OTLP intake.
- **API-based integration** — for SaaS/managed services with no host to
  install an agent on (e.g. third-party billing, managed queue metrics
  exposed via the vendor's API). Pull-based, no agent footprint.

If the discovery notes don't specify a preference and multiple methods would
work, flag it as a clarifying question in Step 2 rather than guessing —
the choice affects network requirements (agent egress vs. Datadog polling
the customer's API) and should be a deliberate decision, not a default.

## Security & networking checklist

Before finalizing the diagram, check the notes for (and ask about anything
missing):

- **Proxy** — does telemetry need to route through an outbound proxy? If so,
  draw it as an explicit node between the collection layer and Datadog
  intake, not an implicit detail.
- **Firewall rules** — are there specific egress rules/allowlisted domains
  required for Datadog intake? Note the relevant Datadog domains if the
  customer needs to open firewall rules (varies by region — confirm with the
  customer's confirmed region rather than assuming).
- **PrivateLink** — is the customer using AWS PrivateLink (or equivalent) to
  avoid public internet egress for telemetry? If so, this materially changes
  the diagram: draw a PrivateLink endpoint between the customer's VPC and
  Datadog's intake rather than a direct arrow.

Draw these as their own layer/overlay on the diagram rather than folding them
into the data-flow arrows — a reviewer should be able to see the security
posture at a glance without tracing every arrow.

## Final diagram organization

When rendering (Step 4), organize the canvas as:

1. Group nodes by **Service Scope** first (e.g. "Production," "Staging," or
   by business unit if the customer's notes are organized that way).
2. Within each scope, arrange **Infrastructure → Application → UI** as
   distinct visual bands (top-to-bottom or left-to-right — pick one and stay
   consistent).
3. Draw data-flow arrows from each node to the Datadog intake, labeled with
   telemetry type and region.
4. Overlay security/networking elements (proxy, firewall, PrivateLink) on the
   path between the customer's environment and Datadog intake.
5. Annotate each node with its collection method so the diagram doubles as an
   implementation checklist, not just a topology sketch.
