---
name: creating-eval-plan
description: >-
  Generate modular Evaluation Plan CSV files for Datadog Home Run POC/Trial
  management. Combines solution-area modules (Infrastructure, APM, Logs, Cloud
  SIEM, LLM Observability, NDM, RUM, Synthetics, CCM, Security, DBM, Incident
  Management, BitsAI, Service Management) into a 4-column CSV (Depth, Title,
  Description, Success Criteria) ready for upload to Home Run. Use when the user
  asks to create an evaluation plan, eval plan, POC plan, trial plan, Home Run
  template, or mentions "evaluation plan", "eval plan", "POC plan", "Home Run
  CSV", or "trial template".
version: "0.4.0"
author: productivity-plugins
tags: eval-plan, evaluation-plan, poc, home-run, csv, sales
---

# Evaluation Plan Generator

Generate modular Evaluation Plan CSV files for Datadog Home Run by combining solution-area template modules. Output is a 4-column CSV ready for direct upload to Home Run.

## CSV Schema

The Home Run CSV upload requires exactly 4 columns:

| Column | Description | Example |
|---|---|---|
| **Depth** | Hierarchical level | `1`, `1.1`, `1.1.1`, `2.1.3` |
| **Title** | Scenario name (include specific versions) | `Deploy Datadog Agent on Windows Server 2019` |
| **Description** | Detailed description, may include doc URLs | `https://docs.datadoghq.eu/agent/...` |
| **Success Criteria** | How to validate completion | `Agent reporting metrics in Datadog` |

## Available Solution Modules

Each module is a standalone CSV template in `references/`. Read the relevant template files when composing an Evaluation Plan. Template URLs default to EU region (datadoghq.eu); substitute the correct domain based on the customer's Datadog region.

| Module File | Solution Area | When to Include |
|---|---|---|
| `infrastructure-monitoring.csv` | Infrastructure Monitoring | Agent deployment (specify OS version e.g. Windows Server 2019, Ubuntu 24.04 LTS), cloud integrations (AWS/Azure/GCP), Kubernetes |
| `apm.csv` | APM | Application tracing (specify language version and framework e.g. Java 21 with Spring Boot 3, Python 3.12 with FastAPI, .NET Core 8 with ASP.NET Core), profiling, runtime metrics |
| `log-management.csv` | Log Management | Log collection, pipelines, indexes, archiving, Logging Without Limits |
| `cloud-siem.csv` | Cloud SIEM | Security log ingestion, detection rules, investigation, SOAR workflows |
| `synthetics.csv` | Synthetic Monitoring | API tests, browser tests, private locations |
| `rum.csv` | Real User Monitoring | Browser RUM, mobile RUM, session replay, RUM-APM correlation |
| `network-monitoring.csv` | Network Monitoring | CNM/NPM, NDM (SNMP), NetFlow, DNS monitoring |
| `cloud-cost-management.csv` | Cloud Cost Management | AWS/Azure/GCP/OCI cost, SaaS costs, cost allocation, tag pipelines |
| `incident-management.csv` | Incident Management | Incident workflows, integrations, timeline, response |
| `bits-ai-sre.csv` | Bits AI for SRE | AI-powered investigation, Dev Agent, MCP Server |
| `llm-observability.csv` | LLM Observability | LLM tracing, evaluations, experiments, prompt management |
| `security-csm.csv` | Cloud Security (CSM) | CSPM, Workload Security, Application Security, Identity Risks |
| `database-monitoring.csv` | Database Monitoring | Specify DB type and version e.g. PostgreSQL 16.2, MySQL 8.0, MS SQL 2019, Oracle 19c, MongoDB 7.0 |
| `dashboards-alerting.csv` | Dashboards & Alerting | Custom dashboards, SLOs, monitors, anomaly/outlier/forecast detection |
| `service-management.csv` | Service Management | Service Catalog, Case Management, On-Call, Workflows/SOAR |
| `poc-wrapper.csv` | POC Wrapper (full lifecycle) | Scoping & alignment (Phase 0), account signup (Phase 1), Datadog setup & data collection (Phase 2), Datadog UI (Phase 3), POC review (Phase 4) |
| `IMPLEMENTATION_GUIDE.md` | Implementation Guide template | Markdown template for Step 6: customer-facing step-by-step guide with structure, generation rules, and appendices |

## Core Workflow

### Step 1: Gather Requirements

Ask the user (or infer from context):

1. **Customer name** — for file naming
2. **Datadog region** — which Datadog site will the customer use? This determines all URLs in the Evaluation Plan:
   - **EU** → `datadoghq.eu` (e.g. `https://www.datadoghq.eu/`, `https://app.datadoghq.eu/`, `https://docs.datadoghq.eu/`, `https://ip-ranges.datadoghq.eu/`)
   - **US1** → `datadoghq.com` (e.g. `https://www.datadoghq.com/`, `https://app.datadoghq.com/`, `https://docs.datadoghq.com/`, `https://ip-ranges.datadoghq.com/`)
   - **US5** → `us5.datadoghq.com` (e.g. `https://us5.datadoghq.com/`, `https://docs.datadoghq.com/`)
   - **AP1** → `ap1.datadoghq.com` (e.g. `https://ap1.datadoghq.com/`, `https://docs.datadoghq.com/`)
3. **Solution areas in scope** — which Datadog products are being evaluated?
4. **POC type** — focused (single solution) or comprehensive (multi-product)?
5. **Technology stack with specific versions:**
   - **Programming languages with version and framework** — e.g. ".NET Core 8 with ASP.NET Core" not just ".NET", "Python 3.12 with FastAPI" not just "Python", "Java 21 with Spring Boot 3" not just "Java"
   - **Operating systems with version** — e.g. "Windows Server 2019" not just "Windows", "Ubuntu 24.04 LTS" not just "Linux", "Amazon Linux 2023" not just "Amazon Linux"
   - **Databases with version** — e.g. "MS SQL 2019" not just "SQL Server", "PostgreSQL 16.2" not just "PostgreSQL"
   - **Specific cloud services** — e.g. "AWS ELB, EC2 M5 xlarge, S3" not just "AWS"
   - **Specific log sources** for Cloud SIEM
   - **Specific LLM providers** for LLMObs
6. **Customer-specific success criteria** — any custom requirements beyond defaults?

### Step 2: Read Template Modules

Read the relevant template CSV files from the `references/` directory based on the solution areas identified in Step 1.

**For a focused POC** (single solution area):
- Read only the specific module CSV
- Optionally wrap with `poc-wrapper.csv` phases

**For a comprehensive POC** (multi-product):
- Read `poc-wrapper.csv` as the skeleton
- Read each solution module needed
- Insert modules into Phase 2 (Datadog Setup & Data Collection) of the wrapper

### Step 3: Compose the Evaluation Plan

Combine the selected modules into a single CSV with proper depth renumbering:

**3a. Depth Renumbering Rules:**
- When inserting modules into a wrapper, renumber the top-level depth of each module to fit the wrapper's hierarchy
- Example: If modules go under Phase 2: Datadog Setup & Data Collection (depth `3` in the wrapper), the first module's `1` becomes `3.1`, its `1.1` becomes `3.1.1`, etc.
- Maintain the relative hierarchy within each module

**3b. Version Specificity Rules:**
- Always include the specific programming language version and framework in titles. Write "Install Datadog .NET Tracing Client (.NET Core 8 / ASP.NET Core)" not "Install the Datadog .NET Tracing Client"
- Always include the OS version in OS-specific titles. Write "Deploy Datadog Agent on Windows Server 2019" not "Deploy Datadog Agent on Windows"
- Always include the database version in DB-specific titles. Write "Enable Database Monitoring for MS SQL 2019" not "Enable Database Monitoring for SQL Server"
- This precision matters because different versions have different setup steps, agent compatibility requirements, and known issues

**3c. Region-Specific URL Rules:**
- Use the customer's Datadog region to determine the correct domain for all URLs
- Template CSVs default to EU region (`datadoghq.eu`). If the customer uses a different region, substitute all URLs accordingly:
  - EU: `datadoghq.eu` (no change needed)
  - US1: replace `datadoghq.eu` with `datadoghq.com`
  - US5: replace `app.datadoghq.eu` with `us5.datadoghq.com`, keep `docs.datadoghq.com`
  - AP1: replace `app.datadoghq.eu` with `ap1.datadoghq.com`, keep `docs.datadoghq.com`
- The signup URL should clearly indicate the region. For EU: "Sign Up for a Datadog Account in EU" with `https://www.datadoghq.eu/`
- IP ranges URL must match the region: `https://ip-ranges.datadoghq.eu/` for EU, `https://ip-ranges.datadoghq.com/` for US

**3d. Customization:**
- Replace placeholder text like `[Customer Source 1]` with actual customer source names
- Add customer-specific success criteria where defaults are empty
- Remove items marked as optional/informational if the customer doesn't need them
- Add customer-specific scenarios not covered by templates

**3e. Pruning:**
- For APM: only include the programming languages the customer uses (with their specific version and framework)
- For Infrastructure: only include the cloud providers and OS versions the customer uses
- For Cloud SIEM: customize log sources to match customer's security stack
- For LLMObs: only include the LLM providers the customer uses
- For DBM: only include the database types and versions the customer uses
- For Network: only include NDM/CNM/NetFlow sections relevant to the customer
- For RUM: only include platforms (browser/iOS/Android) the customer needs

### Step 4: Output the CSV

Write the final CSV to the customer's working directory:

```
eval-plan/<CUSTOMER_NAME>/evalplan_<solution-area>.csv
```

Or for comprehensive plans:
```
eval-plan/<CUSTOMER_NAME>/evalplan_comprehensive.csv
```

**CSV output rules:**
- Header row: `Depth,Title,Description,Success Criteria`
- Quote fields that contain commas or newlines with double quotes
- Escape internal double quotes by doubling them (`""`)
- No trailing commas
- UTF-8 encoding

### Step 5: Validate

After generating the CSV:
1. Verify the 4-column schema is correct
2. Verify depth numbering is sequential and properly nested
3. Verify all URLs use the correct Datadog region domain
4. Verify titles include specific versions (language, OS, DB) where applicable
5. Report the total scenario count to the user

### Step 6: Generate Implementation Guide (Markdown)

After validating the CSV, generate a customer-facing **Implementation Guide** in Markdown. This document is designed to be shared directly with the customer team so they can follow the Evaluation Plan step-by-step without needing Datadog Home Run access.

**Read the template first:** `references/IMPLEMENTATION_GUIDE.md` — this is the structural reference with embedded generation rules in HTML comments.

Write the guide to:
```
eval-plan/<CUSTOMER_NAME>/IMPLEMENTATION_GUIDE.md
```

**Formatting principles:**
- Write for the **customer engineer** who will execute — not the Datadog SE
- Use plain language; avoid Datadog internal jargon
- Each step: a short sub-heading + 1–3 sentence instruction + config snippet (only when it materially helps) + docs link
- Group steps into phases that match the Evaluation Plan hierarchy
- Include doc links inline so the reader can click-through immediately
- Add success criteria as a `> **✅ Validate:**` block at the end of each sub-section
- Omit `[Informational]` items from steps — fold them into a `#### References` list at the section end
- Group `(Debug)` items into a collapsed `<details><summary>Troubleshooting</summary>` block
- Include specific versions in all step titles (OS, language, framework, DB)
- Use the correct Datadog region domain in all URLs

**Generation rules — CSV → Markdown mapping:**

1. **Parse the generated CSV** — walk the depth hierarchy top-down.
2. **Top-level depths (`1`, `2`, `3` …)** → `## Phase` headings.
3. **Second-level depths (`2.1`, `3.2` …)** → `### Sub-section` headings.
4. **Third-level and deeper** → numbered steps or sub-headings (`####`) with how-to instructions, config snippets where useful, and `Reference: [url]` links.
5. **Description field:**
   - Contains a URL → render as inline `Reference: [link](url)` after the instruction.
   - Contains descriptive text + URL → use text as instruction, append the link.
   - Contains only text → use as the instruction body.
6. **Success Criteria field:**
   - Collect all non-empty criteria from items in a section.
   - Render as `> **✅ Validate:** <criteria joined with · >` at section end.
7. **`[Informational]` / `(Informational)` items** → do NOT render as steps; collect into `#### References` list.
8. **`(Optional)` / `[Optional]` items** → render normally but mark heading with `[Optional]`.
9. **`(Debug)` items** → group into a collapsed `<details>` block titled "Troubleshooting" with diagnostic commands.
10. **Customer-specific customization:**
    - Replace `[Customer Source N]` / `[TBD]` placeholders with actual customer values.
    - Add the customer's notification channel (Webex, Slack, Teams) where relevant.
    - Add customer environment details (host counts, DB names, service names) into instructions.
    - Add an **Environment Summary** table at the top populated from discovery data (include all versions).
    - Add **Appendix: Tag Taxonomy** and **Appendix: Network / Firewall Allowlist** sections at the end.
    - Use the correct Datadog region domain in the Network / Firewall Allowlist.

## Example: Focused Cloud SIEM POC (EU Region)

For a customer evaluating Cloud SIEM with Google Workspace, CrowdStrike, and AWS sources on Datadog EU:

```csv
Depth,Title,Description,Success Criteria
1,Phase 0: Scoping & Alignment,,Alignment on requirements & timelines
1.1,Align on Technical Scope,,
1.2,Align on Success Criteria,,
1.3,Align on Timelines,,
2,Phase 1: Sign Up for a Datadog Account in EU,,
2.1,Sign Up for a Datadog Account in EU,https://www.datadoghq.eu/,Account created in EU region
2.2,Get API Key for Agent Installation,https://app.datadoghq.eu/organization-settings/api-keys,API Key retrieved
3,Phase 2: Datadog Setup & Data Collection,,Configure and validate all requirements
3.1,Ingest & Enrich Logs,https://docs.datadoghq.eu/getting_started/security/cloud_siem/,Logs ingested from all sources
3.1.1,Google Workspace,https://docs.datadoghq.eu/integrations/gsuite/#setup,Google Workspace logs flowing
3.1.2,CrowdStrike Alerts,,CrowdStrike alerts ingested
3.1.3,AWS CloudTrail,,AWS CloudTrail logs flowing
3.2,Detect & Monitor,,Security signals generated
3.2.1,Validate OOTB Rules,https://docs.datadoghq.eu/security/default_rules/?category=cat-cloud-siem,OOTB rules generating signals
3.2.2,Create Custom Detection Rules,,Custom rules active
3.2.3,Validate Coverage with MITRE ATT&CK Map,,Coverage gaps documented
...
```

## Example: LLM Observability POC (Python 3.12 / FastAPI / Gemini on GCP Cloud Run — EU Region)

For a customer evaluating LLMObs with Python 3.12, FastAPI, and Gemini on GCP Cloud Run:

```csv
Depth,Title,Description,Success Criteria
1,Phase 0: Scoping & Alignment — LLM Observability,,Alignment on requirements
1.1,Identify AI Applications in Scope,,Applications inventory documented
1.2,Align on Success Criteria,,Success criteria agreed
1.3,Confirm LLM Request Volume Estimates,,Volume documented for BOQ
2,Phase 1: Sign Up for a Datadog Account in EU,,
2.1,Sign Up for a Datadog Account in EU,https://www.datadoghq.eu/,Account created in EU region
2.2,Get API Key for Agent Installation,https://app.datadoghq.eu/organization-settings/api-keys,API Key retrieved
3,Phase 2: Datadog Setup & Data Collection — Instrumentation,,
3.1,Install ddtrace for Python 3.12,https://docs.datadoghq.eu/llm_observability/setup/auto_instrumentation/?tab=python,LLM spans visible
3.2,Google Gen AI SDK (Vertex AI / Gemini) Integration,,Gemini LLM calls traced
3.3,Correlate LLMObs with APM Traces (FastAPI),,LLMObs linked to APM
4,Phase 3: Datadog UI — Performance Monitoring,,
4.1,Validate LLM Tracing,,All LLM calls traced
4.2,Token Usage & Cost Tracking,,Cost metrics visible
...
```

## Reference: Confluence Product Wiki Pages

When the user needs deeper product context, search Confluence (GTMSEH space) for:

- **LLM Observability:** page ID `3784344500` — pricing, value props, HIPAA, data privacy
- **Cloud SIEM:** page ID `1343389792` — TDIR capabilities, OOTB rules, MITRE ATT&CK
- **General product wikis:** space `GTMSEH` — search by product name

Use Atlassian MCP CQL search:
```
space = "GTMSEH" AND title ~ "<product name>" AND type = page
```

## Reference: LLM Observability Pricing (from Confluence)

- Minimum commitment: 100,000 LLM requests at $80/month
- Additional requests above 100K: $8 per 10,000 LLM requests
- No other Datadog product required
- HIPAA eligible (since April 2025)
- Sensitive Data Scanner included with LLMObs
- OOTB evaluations require customer's own OpenAI/Anthropic/Bedrock keys (BYOK)
- Custom LLM-as-a-Judge supports: OpenAI, Anthropic, Bedrock, Vertex AI (Gemini), Azure OpenAI, AI Gateway
- Experiments and Datasets included in LLMObs entitlement

## Reference: LLMObs Evaluation Capabilities

| Evaluation Type | Framework Required? | Gemini/Vertex Support? | Notes |
|---|---|---|---|
| OOTB Managed Evals | None (managed by DD) | Not supported (OpenAI/Anthropic/Bedrock only) | Automatic, zero code |
| Custom LLM-as-a-Judge | None — fully custom prompt | Vertex AI natively supported | Boolean/Score/Categorical/JSON output |
| RAGAS Integration | RAGAS Python library | Yes (app LLM, not judge) | For RAG pipeline quality |
| External Eval (SDK/API) | Any / None | Yes | Submit from any framework |
