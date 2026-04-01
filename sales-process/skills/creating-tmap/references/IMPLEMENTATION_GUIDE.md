# <CUSTOMER_NAME> — Datadog POC Implementation Guide

**Customer:** <CUSTOMER_NAME>
**Solution Areas:** <list of solution areas, e.g. Infrastructure · APM · Log Management>
**Datadog Region:** <EU / US1 / US5 / AP1>
**Prepared by:** Datadog SE Team
**Last Updated:** <DATE>

---

## Environment Summary

<!-- Populate from customer discovery / TMAP scoping. Be specific about versions. -->

| Component | Details |
|---|---|
| **Hosts** | <count, OS with version e.g. Windows Server 2019, Ubuntu 24.04 LTS> |
| **Application** | <app name, language with version and framework e.g. .NET Core 8 with ASP.NET Core, Python 3.12 with FastAPI> |
| **Database** | <type with version e.g. MS SQL 2019, PostgreSQL 16.2> |
| **Cloud** | <AWS / Azure / GCP / OCI — services used> |
| **Containers** | <orchestrator, count> |
| **Network Devices** | <vendor, model> |
| **Alert Channel** | <Slack / Teams / Webex / PagerDuty / etc.> |
| **Log Volume** | <estimated GB/month, retention> |

---

## Table of Contents

<!-- Auto-generate from TMAP phases. One entry per Phase / sub-section. -->

1. [Phase 0 — Scoping & Alignment](#phase-0--scoping--alignment)
2. [Phase 1 — Sign Up for a Datadog Account](#phase-1--sign-up-for-a-datadog-account)
3. [Phase 2 — Datadog Setup & Data Collection](#phase-2--datadog-setup--data-collection)
4. [Phase 3 — Datadog UI](#phase-3--datadog-ui)
5. [Phase 4 — POC Review & Close](#phase-4--poc-review--close)
6. [Appendix: Tag Taxonomy](#appendix-tag-taxonomy)
7. [Appendix: Network / Firewall Allowlist](#appendix-network--firewall-allowlist)

---

## Phase 0 — Scoping & Alignment

### Technical Scope

<!-- Populate from TMAP Phase 1 / Scoping rows -->

| Area | Scope |
|---|---|
| Infrastructure | <details including OS versions e.g. Windows Server 2019> |
| APM | <details including language versions and frameworks e.g. .NET Core 8 with ASP.NET Core> |
| Database | <details including DB type and version e.g. MS SQL 2019> |
| Logs | <details> |
| Network | <details> |
| Alerting | <details> |

### Success Criteria Checklist

<!-- Convert TMAP Success Criteria fields into checkboxes -->

- [ ] <success criteria 1 from TMAP>
- [ ] <success criteria 2 from TMAP>
- [ ] ...

### Prerequisites Checklist

- [ ] AWS / Azure / GCP IAM permissions for integration deployment
- [ ] SSH / RDP access to target hosts (or config management tool for bulk install)
- [ ] Database monitoring user credentials
- [ ] SNMP community strings for network devices (if NDM in scope)
- [ ] Notification channel webhook URL (Slack / Teams / Webex)
- [ ] Outbound port 443 allowed to `*.datadoghq.eu` — [IP Ranges](https://ip-ranges.datadoghq.eu/)

---

## Phase 1 — Sign Up for a Datadog Account

### Create Datadog Account

1. Go to the Datadog signup page for your region (e.g. [https://www.datadoghq.eu/](https://www.datadoghq.eu/) for EU) and sign up for a trial.
2. Confirm the Datadog region with your Datadog SE (EU / US1 / US5 / AP1).
3. Complete email verification.

### Retrieve API Key

1. Navigate to **Organization Settings → API Keys**: [link](https://app.datadoghq.eu/organization-settings/api-keys)
2. Click **+ New Key** → name it `<customer>-poc-agent`.
3. Copy and securely share the API key with the infrastructure team.

---

## Phase 2 — Datadog Setup & Data Collection

<!-- ============================================================
     GENERATION RULES — how to render each TMAP section:

     For EACH sub-section under Phase 2 in the TMAP CSV:

     1. Create a ### heading with the section number and title.
        Include specific versions in titles, e.g.:
        "Deploy Datadog Agent on Windows Server 2019" not "Deploy Datadog Agent on Windows"
        "Install .NET Core 8 Tracing Client" not "Install .NET Tracing Client"

     2. For each actionable step (depth 3+):
        - Write a short sub-heading or numbered step.
        - Include 1–3 sentences of HOW-TO instruction.
        - Include config snippets / commands where they help.
        - End with "Reference: [url]" linking to the docs.
        - Use the correct Datadog region domain in all URLs.

     3. Items prefixed with (Informational) or [Informational]:
        - Do NOT render as steps.
        - Collect into a "#### References" list at the section end.

     4. Items prefixed with (Optional) or [Optional]:
        - Render normally but mark the heading with [Optional].

     5. Items prefixed with (Debug):
        - Group into a "### Troubleshooting" sub-section at the
          end of their parent section. Include diagnostic commands.

     6. After each section, add a validation block:

        > **✅ Validate:** <success criteria from the TMAP>

     ============================================================ -->

### 2.X <Section Title from TMAP>

<!-- Step-by-step for each item at depth 3+ -->

#### <Step Title — include version specifics>

<1–3 sentence instruction. What to do and where.>

```bash
# config snippet or command — only when it materially helps the reader
<example command>
```

Reference: [docs link](https://docs.datadoghq.eu/...)

#### <Next Step Title>

<instruction>

Reference: [docs link](https://docs.datadoghq.eu/...)

> **✅ Validate:** <success criteria collected from this section's TMAP rows>

#### References

- [<Informational item title>](<url>)

<details>
<summary>Troubleshooting</summary>

#### <Debug Step Title>

<diagnostic instruction and commands>

```bash
<diagnostic command>
```

Reference: [docs link](https://docs.datadoghq.eu/...)

</details>

---

<!-- Repeat ### 2.X block for each solution area sub-section -->

## Phase 3 — Datadog UI

Schedule a **30–45 minute walkthrough** with the customer team for each area:

| Session | Items to Review | Attendees |
|---|---|---|
| <area 1> | <what to check> | <who should attend> |
| <area 2> | <what to check> | <who should attend> |

---

## Phase 4 — POC Review & Close

### Success Criteria Validation

<!-- Mirror the success criteria from Phase 1 with pass/fail -->

| Success Criteria | Status |
|---|---|
| <criteria 1> | ☐ Pass / ☐ Fail |
| <criteria 2> | ☐ Pass / ☐ Fail |

### POC Playback / Showback

Prepare a presentation covering:

1. **Before / After** — what was invisible before Datadog, what is now visible
2. **Key Findings** — top issues discovered during the POC
3. **Incidents Caught** — real problems surfaced by Watchdog or monitors

### Commercial Alignment

| Product | Quantity | Unit |
|---|---|---|
| <product 1> | <qty> | <unit> |
| <product 2> | <qty> | <unit> |

---

## Appendix: Tag Taxonomy

| Tag Key | Values | Applied To |
|---|---|---|
| `env` | `prod`, `uat`, `dev` | All hosts, containers, logs, APM |
| `service` | `<service names>` | All resources |
| `team` | `<team name>` | All resources |
| `version` | `<app version>` | APM service tags |

---

## Appendix: Network / Firewall Allowlist

| Destination | Port | Protocol | Purpose |
|---|---|---|---|
| `*.datadoghq.eu` | 443 | TCP/HTTPS | Agent → Datadog API (metrics, traces, logs) |
| `agent-http-intake.logs.datadoghq.eu` | 443 | TCP/HTTPS | Log ingestion |
| `trace.agent.datadoghq.eu` | 443 | TCP/HTTPS | APM trace ingestion |
| `process.datadoghq.eu` | 443 | TCP/HTTPS | Process metrics |

Full IP range: [https://ip-ranges.datadoghq.eu/](https://ip-ranges.datadoghq.eu/)

---

*Document prepared by Datadog SE for <CUSTOMER_NAME> POC*
