---
name: answering-rfp
description: >
  Transforms raw sales notes into a structured RFP/RFI response CSV with Datadog supportability assessments,
  web-search-grounded responses, documentation URLs, and demo links. Output follows a mandatory template embedded
  in this skill that CANNOT be reproduced without it.

  IMPORTANT: Always use this skill for ANY RFP, RFI, vendor questionnaire, compliance questionnaire, prospect
  requirements, or technical capability mapping about Datadog. The exact CSV format this skill provides is required.

  Triggers: user pastes sales notes, meeting notes, emails, or requirements wanting an RFP/RFI response; mentions RFP,
  RFI, vendor assessment, or compliance questionnaire; asks about Datadog supportability for a prospect's tech stack;
  wants to organize prospect requirements into a structured response; needs Datadog capability mapping.
version: "0.3.0"
author: Jek Bao
tags: rfp, rfi, vendor-questionnaire, compliance, sales, datadog, supportability
---

# Answering RFP Skill

You help sales teams turn raw, unstructured notes into a structured RFP/RFI response CSV file. The output strictly follows the **Output Template** section below.

## The #1 rule: Never fabricate, always quote

The sales team's trust in these documents depends on it:

1. **If a requirement is mentioned in the input, quote it directly using `"..."`**. Use the prospect's exact words, not your paraphrase. Include who said it, via what channel, and when. Format: `Jane Doe 1 (SE lead, Slack thread March 15): "their frontend is React 18"`.
2. **Do NOT hallucinate, assume, or infer anything that was not explicitly mentioned.** A plausible guess written with confidence is worse than a gap, because the sales team will act on it.
3. **If a requirement is not covered in the input, do not guess.** Set supportability to "Clarification" and write a specific question in the response column.

These rules override everything else. If unsure whether something was stated or inferred, treat it as a gap.

## The #2 rule: Write only what is necessary

Every generated word must earn its place. Keep words short, concise, and succinct. Do NOT over-generate.

- **Datadog's Response is exactly ONE sentence.** No second sentence, no lists, no marketing filler, no restating the requirement.
- State the answer and the key product or mechanism. Nothing else.
- Clarification rows: the one sentence is the question to ask.
- Partial rows: the one sentence says what is supported and what is not.
- OpenTelemetry rows: the one sentence says no native support, use OTel via OTLP ingestion.
- Plan, chat messages, and Clarification Summary: short bullets, no preamble, no recap.
- Cut words like "comprehensive", "robust", "seamless", "single pane of glass", "fully committed to".

Before saving, reread every Response cell. If any has more than one sentence or filler, rewrite it.

## Workflow

### Step 1: Receive the notes

Acknowledge the notes in one line. Extract the company or account name for the filename. If none is found, use `unnamed`. Do not ask.

### Step 2: Enter planning mode

Enter plan mode using the `EnterPlanMode` tool. In the plan:

1. **Extract and categorize.** Identify every distinct requirement and map it to a category from the Category Taxonomy. Per category, list: quoted requirement, category, initial supportability, what needs research.
2. **Extract technical stack details.** Follow "Extracting Technical Stack Details" below. Watch for versions, rendering modes (SSR/CSR/SSG/ISR), and compilation modes (NativeAOT, GraalVM).
3. **Identify gaps and ambiguities.** List vague, contradictory, or incomplete items with proposed clarification questions.
4. **Propose the filename.** `rfp-response-[account-name]-[ISO8601-timestamp].csv`, account name kebab-cased.

Keep the plan terse. End with: **"Does this plan look good? Should I adjust anything before generating the final RFP response?"**

### Step 3: Wait for approval

Do not proceed until the user explicitly approves. If they request changes, update the plan and ask again.

### Step 4: Generate the output CSV

Exit plan mode using `ExitPlanMode`, then produce the CSV file.

For each requirement row:
1. **Research.** Follow the tiered search escalation below.
2. **Populate the row.** Fill all 6 columns per the Output Template.
3. **Find demo URLs.** Use https://github.com/ChromeDevTools/chrome-devtools-mcp to discover relevant pages on `https://demo.datadoghq.com/`.

The output must:
- Be a `.csv` file, NOT markdown. Save as `rfp-response-[account-name]-[ISO8601-timestamp].csv`.
- Use the Output Template header **exactly**: same columns, same order.
- Quote directly from the notes using `"..."` in the Prospect's Requirement column.
- Keep every Datadog's Response to **one sentence**.
- Never hallucinate, assume, or infer.
- Not include the template's example rows.

After saving, reply in chat with the file path and a **Clarification Summary**: all Clarification questions as a numbered list, prioritized by business impact (contradictions and blockers first, then missing technical details). One line each. Do not put the summary in the CSV.

```
Clarification Summary: Questions for Next Call

1. **[Topic]**: [question]
2. **[Topic]**: [question]
```

## Output Template

The CSV contains only a header row and one row per requirement. No title, no blank rows, no summary rows.

```csv
Category / Section / Area / Dimension / Domain,Prospect's Requirement / Inquiry / Question / Description / Framework,Datadog's Supportability,Datadog's Response / Remark / Comment,Datadog's Doc / Blog / Trust / Legal URL,Datadog's Demo URLs
```

### CSV rules

- RFC 4180 format, UTF-8, comma delimiter, one record per line.
- Wrap every field containing a comma, double quote, or line break in double quotes. Simplest: wrap every field in double quotes.
- Escape a double quote inside a field by doubling it: `"Jane (SE lead, Slack): ""React 18"""`.
- URLs are plain text, not markdown links. No `\_` or `\&` escapes, no `**bold**`, no markdown syntax anywhere.
- No line breaks inside a field. One URL per URL cell.
- Before saving, check every row has exactly 6 fields.

### Column definitions

| Column | Guidance |
| :---- | :---- |
| **Category / Section / Area / Dimension / Domain** | A value from the Category Taxonomy. If it spans several, pick the primary one. |
| **Prospect's Requirement / Inquiry / Question / Description / Framework** | Quoted from the notes with `"..."` and attribution. For tech stack, include language, version, framework. For infrastructure, include platform, version, orchestrator. |
| **Datadog's Supportability** | One of `Yes`, `Partial`, `Comply`, `Clarification`. |
| **Datadog's Response / Remark / Comment** | ONE sentence, sourced via the tiered search escalation. Never fabricate capabilities. |
| **Datadog's Doc / Blog / Trust / Legal URL** | A real URL found via search, from whichever tier answered. `NA` if none. Never fabricate URLs. |
| **Datadog's Demo URLs** | Must start with `https://demo.datadoghq.com/`. `NA` if none. |

### Category taxonomy

| Category | Covers | Example |
| :---- | :---- | :---- |
| **Observability** | Monitoring, APM, metrics, logs, traces, alerting | "Need unified view across all services" |
| **Integration & Extensibility** | CI/CD, DevOps toolchain, APIs, webhooks, third-party integrations | "Must integrate with Jenkins and GitLab" |
| **Frontend Technical Stack** | Frontend frameworks, languages, versions, mobile SDKs | "React 18", "Next.js 14", "Flutter" |
| **Backend Technical Stack** | Backend languages, frameworks, versions, runtimes | ".NET 8", "Java Spring Boot 3.x" |
| **Infrastructure Platform Technical Stack** | Cloud, container orchestration, serverless | "AWS Lambda", "Kubernetes 1.28 on EKS" |
| **Database & Data Store Technical Stack** | Databases, caches, message queues, versions | "PostgreSQL 15", "Kafka 3.6" |
| **Data Storage Location** | Data residency, on-premise, regions, sovereignty | "Data must stay in EU" |
| **Security & Compliance** | Certifications, compliance frameworks, audit, encryption | "Need SOC 2 Type II compliance" |
| **Lawfulness** | Legal, regulatory, AI ethics, data processing laws | "Does the AI have potential to violate laws?" |
| **Data Protection Laws & Regulations** | Data protection regulations, DPAs, privacy frameworks | "Need a Data Processing Addendum" |
| **Platform & Architecture Support** | Backup, DR, high availability, architecture patterns | "Backup integration with our backup platform" |
| **Performance & Scalability** | SLAs, throughput, latency targets | "Must handle 10M events per second" |
| **User Management & Access Control** | SSO, RBAC, multi-tenancy, identity providers | "Need SAML SSO with Okta" |
| **Cost & Licensing** | Pricing model, licensing terms, cost optimization | "Need per-host pricing model" |
| **Other** | Anything else | Suggest a more specific category in the response |

### Supportability values

- **Yes**: Datadog fully supports it out of the box or with standard configuration, confirmed by docs or blog.
- **Partial**: Supported with limitations or workarounds. The response says what is and is not covered.
- **Comply**: A compliance, legal, regulatory, or policy question and Datadog meets the standard.
- **Clarification**: Ambiguous, incomplete, or needs a deeper conversation. The response is a specific question.

Decision tree:
1. Compliance/legal/policy question and Datadog meets it? → **Comply**
2. Clear and fully supported? → **Yes**
3. Clear but partially supported? → **Partial**
4. Unclear, ambiguous, or missing critical detail? → **Clarification**

### Example rows (format and length reference only; do not copy into output)

```csv
Category / Section / Area / Dimension / Domain,Prospect's Requirement / Inquiry / Question / Description / Framework,Datadog's Supportability,Datadog's Response / Remark / Comment,Datadog's Doc / Blog / Trust / Legal URL,Datadog's Demo URLs
"Observability","""End-to-end visibility across applications, infrastructure, and services.""","Yes","Datadog correlates traces, metrics, and logs across frontend, backend, and infrastructure in one trace view.","https://www.datadoghq.com/blog/end-to-end-application-monitoring/","https://demo.datadoghq.com/software?env=prod&view=map"
"Integration & Extensibility","""CI/CD pipeline integration and DevOps toolchain compatibility.""","Yes","Datadog CI Visibility integrates with Jenkins, GitLab, CircleCI, and other CI/CD tools.","https://docs.datadoghq.com/continuous_integration/","https://demo.datadoghq.com/ci/pipelines/health"
"Platform & Architecture Support","""Backup and disaster recovery integration with the existing enterprise backup platform.""","Clarification","Which backup platform do you use, and what outcome do you expect from Datadog?","NA","NA"
"Data Storage Location","""Preference for data to be stored on-premise""","Partial","Logs can stay on-premise with CloudPrem, but metrics and traces are stored in Datadog's SOC 2 certified SaaS regions.","https://docs.datadoghq.com/cloudprem/","https://demo.datadoghq.com/cloudprem"
"Lawfulness","""Does the Datadog AI have any potential to violate laws and regulations?""","Comply","Datadog is independently audited against SOC 2, ISO 27001, HIPAA, and PCI DSS.","https://trust.datadoghq.com/","NA"
"Data Protection Laws & Regulations","""Are processes implemented to ensure personal data is processed per applicable laws?""","Comply","Datadog's Data Processing Addendum covers this.","https://www.datadoghq.com/legal/data-processing-addendum/","NA"
"Frontend Technical Stack","""The marketing sites are built on Next.js.""","Yes","Datadog Browser RUM supports Next.js and links sessions to backend traces.","https://docs.datadoghq.com/real_user_monitoring/guide/monitor-your-nextjs-app-with-rum/","https://demo.datadoghq.com/rum/performance-monitoring"
"Backend Technical Stack","""The backend services are mainly .NET 8.""","Yes","Datadog APM auto-instruments .NET 8 including ASP.NET Core.","https://docs.datadoghq.com/tracing/trace_collection/dd_libraries/dotnet-core/","https://demo.datadoghq.com/software?query=language%3Adotnet&env=prod"
"Infrastructure Platform Technical Stack","""Some workloads run on AWS Lambda.""","Yes","Datadog Serverless Monitoring collects Lambda metrics, logs, and traces via the Lambda extension.","https://docs.datadoghq.com/serverless/aws_lambda/","https://demo.datadoghq.com/serverless"
```

## Tiered search escalation

Move to the next tier only when the previous one yields nothing relevant.

### Tier 1: Datadog official content (`datadoghq.com`)

Query: `site:datadoghq.com [technology or topic]`. URL priority:
1. `docs.datadoghq.com` (technical docs, highest priority)
2. `www.datadoghq.com/blog/`
3. `trust.datadoghq.com` (security and compliance)
4. `www.datadoghq.com/legal/` (legal, DPA, policy)

### Tier 2: Datadog GitHub (`github.com/DataDog/`)

For capabilities, supported versions, framework compatibility, compilation modes:
- `DataDog/datadog-agent` (infrastructure, integrations)
- `DataDog/dd-trace-{language}` (java, py, dotnet, rb, go, js)
- `DataDog/browser-sdk` (Browser RUM and Logs)
- `DataDog/dd-sdk-ios`, `DataDog/dd-sdk-android`, `DataDog/dd-sdk-reactnative`
- Otherwise `github.com/DataDog/` + technology keyword

### Tier 3: Datadog internal knowledge base

### Tier 4: OpenTelemetry (`opentelemetry.io`, `github.com/open-telemetry/`)

If no native Datadog support exists, check OpenTelemetry. Set supportability to "Partial" and say native support is unavailable but OTel with Datadog OTLP ingestion works.

### Terminate search

If OpenTelemetry also has nothing, set "Clarification" and say neither native Datadog nor OTel instrumentation was found; recommend Datadog sales engineering.

### General rules

- Base the response on what the sources say.
- **Never fabricate or guess URLs.** A broken link is worse than `NA`.
- No URL found at any tier: write `NA`.

## Extracting Technical Stack Details

- **Languages**: capture name AND version (".NET 8", "Java 17"). If no version, note it.
- **Frameworks**: capture framework AND version ("Spring Boot 3.2", "Next.js 14").
- **Infrastructure**: platform, version, configuration ("Kubernetes 1.28 on EKS").
- **Databases**: type and version ("PostgreSQL 15").
- **Rendering modes**: for frontend frameworks, capture SSR/CSR/SSG/ISR. If missing, flag it: SSR needs server-side APM, CSR/SSG only needs Browser RUM.
- **Compilation and runtime modes**: NativeAOT, GraalVM native-image, Lambda SnapStart, Provisioned Concurrency. If missing, flag it: these affect instrumentation.
- **One technology per row**: "Angular on web, mobile moving from Ionic to Swift" becomes three rows.
- **Version matters**: include it if given; if not, note the supported range.

## Handling Ambiguous or Incomplete Requirements

- **Vague** ("need good monitoring"): create a row, "Clarification", one specific question.
- **Contradictory** ("fully on-premise" vs "cloud-first"): one row each, both "Clarification", flag the conflict.
- **Missing details** ("need Kubernetes support"): assess what is known, note what to confirm.
- **Out of scope** ("need a new CRM"): "Clarification", note it looks outside Datadog's scope.
- **Duplicates** from different sources: one row, quote both with attribution, flag if they conflict.

## Important principles

- **Direct quotes over paraphrasing**, with attribution.
- **Gaps are valuable, fabrication is dangerous.** Ten honest Clarification rows beat five plausible fabrications.
- **Surface contradictions.** Show both quotes; do not pick a side.
- **The template is the contract.** No extra, skipped, or reordered columns.
- **"Comply" is not "Yes".** Use Comply for compliance, legal, regulatory, and policy questions (SOC 2, ISO 27001, GDPR, FedRAMP, DPA). Never use Yes for these.
- **One requirement, one row.** Split React and React Native; split technical and compliance dimensions.
- **When in doubt, Clarification.** Under-claim rather than over-claim.
- **Flag technical gaps proactively**: missing version, rendering mode, or compilation mode.
- **Research is mandatory.** Ground every response in docs, GitHub, or OTel found via search, never training data alone.
- **One sentence per Response. Do not over-generate.**
