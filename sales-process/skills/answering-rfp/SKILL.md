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
version: "0.4.0"
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

## The #2 rule: Never over-claim Datadog capabilities. If uncertain, skip

A wrong "Yes" can end up in a signed contract. An unanswered row costs nothing.

1. **Claim only what a source explicitly states.** Answer `Yes`, `Partial`, or `Comply` only when a page you actually opened in this session confirms that exact capability, version, framework, region, or certification.
2. **No source URL, no claim.** If the URL cell would be `NA`, the row cannot be `Yes`, `Partial`, or `Comply`.
3. **Match the scope exactly.** Docs for "Java" do not confirm "Java 21 on GraalVM native-image". Docs for "Kubernetes" do not confirm "OpenShift 4.14". A blog announcing a beta or preview does not confirm general availability. If the source does not name the specific item, it is not confirmed.
4. **Do not stretch the response beyond the source.** No extra versions, limits, features, regions, SLAs, certifications, or product names that the cited page does not state. No "and other tools" unless the page lists them.
5. **Do not answer from training data or memory.** If search did not confirm it, it is not confirmed, however sure you feel.
6. **If uncertain, skip.** Set supportability to `Skipped`, write `NA` in the Response, Doc, and Demo columns. Do not hedge, guess, or write "likely" or "should".
7. **Compliance, legal, pricing, and SLA questions are the highest risk.** Answer only if the trust, legal, or pricing page states it directly. Otherwise `Skipped`.

`Skipped` (Datadog side unknown) is different from `Clarification` (prospect side unclear). Use `Clarification` only when the prospect's requirement itself is vague or incomplete.

## The #3 rule: Write only what is necessary

Every generated word must earn its place. Keep words short, concise, and succinct. Do NOT over-generate.

- **Datadog's Response is exactly ONE sentence of 25 words or fewer.** No second sentence, no semicolons or dashes chaining clauses, no lists, no marketing filler, no restating the requirement.
- State the answer and the key product or mechanism. Nothing else.
- Flags, caveats, and follow-ups (missing version, rendering mode, conflicts, scope doubts) go in the Clarification Summary, never as extra text in the Response.
- **Prospect's Requirement quote**: the shortest exact span that names the item, plus attribution. Not the whole paragraph.
- Clarification rows: the one sentence is the question to ask.
- Partial rows: the one sentence says what is supported and what is not.
- OpenTelemetry rows: the one sentence says native support was not found, use OTel via OTLP ingestion.
- Skipped rows: Response is `NA`. No explanation.
- Plan, chat messages, and summaries: short bullets or a table, no preamble, no recap, no closing remarks.
- Cut words like "comprehensive", "robust", "seamless", "single pane of glass", "fully committed to".

Before saving, reread every Response cell. If any has more than one sentence, more than 25 words, or filler, rewrite it.

## Workflow

### Step 1: Receive the notes

Acknowledge the notes in one line. Extract the company or account name for the filename. If none is found, use `unnamed`. Do not ask.

### Step 2: Enter planning mode

Enter plan mode using the `EnterPlanMode` tool. In the plan:

1. **Extract and categorize.** Identify every distinct requirement and map it to a category from the Category Taxonomy. Per category, list: quoted requirement, category, initial supportability, what needs research.
2. **Build the tech stack inventory.** Follow "Extracting Technical Stack Details" below. Show it in the plan as a numbered table: `# | Item (with version) | Exact quote | Row category`. Total count at the bottom.
3. **Identify gaps and ambiguities.** List vague, contradictory, or incomplete items with proposed clarification questions.
4. **Propose the filename.** `rfp-response-[account-name]-[YYYY-MM-DDTHHMMSSZ].csv`, account name kebab-cased.

Keep the plan terse. End with: **"Does this plan look good? Should I adjust anything before generating the final RFP response?"**

### Step 3: Wait for approval

Do not proceed until the user explicitly approves. If they request changes, update the plan and ask again.

### Step 4: Generate the output CSV

Exit plan mode using `ExitPlanMode`, then produce the CSV file.

Every inventory item from the approved plan becomes at least one row. For each requirement row:
1. **Research.** Follow the tiered search escalation below.
2. **Populate the row.** Fill all 6 columns per the Output Template.
3. **Find demo URLs.** Use https://github.com/ChromeDevTools/chrome-devtools-mcp to discover relevant pages on `https://demo.datadoghq.com/`. Use only a page you opened that shows the claimed feature; otherwise `NA`. Skipped rows get no demo URL.

The output must:
- Be a `.csv` file, NOT markdown. Save as `rfp-response-[account-name]-[YYYY-MM-DDTHHMMSSZ].csv`.
- Use the Output Template header **exactly**: same columns, same order.
- Quote directly from the notes using `"..."` in the Prospect's Requirement column.
- Keep every Datadog's Response to **one sentence**.
- Never hallucinate, assume, or infer.
- Never over-claim: unconfirmed rows are `Skipped`.
- Not include the template's example rows.

Before saving, run the **coverage check**: tick every inventory item against the CSV. Count of tech stack rows must be at least the inventory count. Add any missing row before saving. Never drop a row because it is Skipped, unclear, or minor. Never add a second row for an item already covered by another row; one item, one row.

Then run the **over-claim check** on every `Yes`, `Partial`, and `Comply` row: does the cited page, opened in this session, explicitly state the exact claim in the Response? If not, or if you are unsure, change the row to `Skipped` with `NA` in the Response, Doc, and Demo columns.

After saving, reply in chat with the file path, a **Clarification Summary**, and a **Skipped Summary**. One line each. Do not put either summary in the CSV.

- Clarification Summary: all Clarification questions as a numbered list, prioritized by business impact (contradictions and blockers first, then missing technical details).
- Skipped Summary: every Skipped requirement, for a Datadog SE to verify before anyone answers it.

```
Clarification Summary: Questions for Next Call

1. **[Topic]**: [question]
2. **[Topic]**: [question]

Skipped Summary: Needs Datadog SE Verification

1. **[Topic]**: [requirement, short]
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
| **Datadog's Supportability** | One of `Yes`, `Partial`, `Comply`, `Clarification`, `Skipped`. |
| **Datadog's Response / Remark / Comment** | ONE sentence, stating only what the cited source says. `NA` for Skipped rows. Never fabricate capabilities. |
| **Datadog's Doc / Blog / Trust / Legal URL** | A real URL found via search that confirms the response. Required for Yes, Partial, and Comply. `NA` for Clarification and Skipped. Never fabricate URLs. |
| **Datadog's Demo URLs** | Must start with `https://demo.datadoghq.com/` and be a page you opened that shows the claimed feature. `NA` if none or if Skipped. |

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
| **Other** | Anything else | "Need a new CRM" |

### Supportability values

- **Yes**: A source explicitly confirms Datadog supports the exact item out of the box or with standard configuration.
- **Partial**: A source explicitly confirms support with stated limitations. The response says what is and is not covered, both per the source.
- **Comply**: A compliance, legal, regulatory, or policy question and a trust or legal page explicitly states Datadog meets it.
- **Clarification**: The prospect's requirement is ambiguous or incomplete. The response is a specific question for the prospect.
- **Skipped**: The requirement is clear, but no source confirms Datadog's support. No answer is given. Response, Doc, and Demo are `NA`.

Decision tree:
1. Requirement vague or incomplete? → **Clarification**
2. No opened source explicitly confirms the exact claim, or any doubt? → **Skipped**
3. Compliance/legal/policy question confirmed by a trust or legal page? → **Comply**
4. Source confirms full support? → **Yes**
5. Source confirms support with stated limits? → **Partial**

### Example rows (format and length reference only; do not copy into output)

```csv
Category / Section / Area / Dimension / Domain,Prospect's Requirement / Inquiry / Question / Description / Framework,Datadog's Supportability,Datadog's Response / Remark / Comment,Datadog's Doc / Blog / Trust / Legal URL,Datadog's Demo URLs
"Observability","""End-to-end visibility across applications, infrastructure, and services.""","Yes","Datadog correlates traces, metrics, and logs across frontend, backend, and infrastructure in one trace view.","https://www.datadoghq.com/blog/end-to-end-application-monitoring/","https://demo.datadoghq.com/software?env=prod&view=map"
"Integration & Extensibility","""CI/CD pipeline integration and DevOps toolchain compatibility.""","Yes","Datadog CI Visibility integrates with Jenkins, GitLab, and CircleCI.","https://docs.datadoghq.com/continuous_integration/","https://demo.datadoghq.com/ci/pipelines/health"
"Platform & Architecture Support","""Backup and disaster recovery integration with the existing enterprise backup platform.""","Clarification","Which backup platform do you use, and what outcome do you expect from Datadog?","NA","NA"
"Data Storage Location","""Preference for data to be stored on-premise""","Partial","Logs can stay on-premise with CloudPrem, but metrics and traces are stored in Datadog SaaS.","https://docs.datadoghq.com/cloudprem/","NA"
"Lawfulness","""Does the Datadog AI have any potential to violate laws and regulations?""","Skipped","NA","NA","NA"
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

Use only if it is actually available in this session and returns a document you can cite. Never treat recollection as Tier 3.

### Tier 4: OpenTelemetry (`opentelemetry.io`, `github.com/open-telemetry/`)

If no native Datadog support is found, check OpenTelemetry. Set "Partial" only if you find an OTel instrumentation page for that exact technology AND cite it. Say native support was not found and OTel via Datadog OTLP ingestion is the path. Do not claim the OTel data has full parity with native.

### Terminate search

If no tier confirms it, set "Skipped" with `NA` in the Response, Doc, and Demo columns, and list it in the Skipped Summary.

### General rules

- Base the response only on what the opened sources say. Search snippets alone are not enough; open the page.
- Not finding a page does not mean Datadog lacks support. Do not answer "No" or "not supported" unless a source says so; use Skipped.
- **Never fabricate or guess URLs.** A broken link is worse than `NA`.
- No URL found at any tier: write `NA`.

## Extracting Technical Stack Details

**Do not miss any item.** Read the notes line by line, twice. On the second pass, look only for named technologies you missed on the first. Capture every named technology, product, tool, or service, including:

- Passing mentions inside sentences about something else ("the Go service that reads from Kafka" is two items: Go, Kafka).
- Both sides of a migration or evaluation ("moving from Ionic to Swift", "considering Aurora") as separate items, labelled current or planned.
- Abbreviations and nicknames ("k8s", "PG", "ECS", "GHA"). Quote as written; name the item in full.
- Items in lists, tables, attachments, diagrams, and pasted architecture text.
- Items with no version and no clear requirement. They still get a row.

Scope to scan for:

- Languages, runtimes, frameworks, and libraries (frontend, backend, mobile).
- Cloud, containers, orchestration, serverless, operating systems, VMs.
- Databases, caches, message queues, streaming, search engines, data warehouses.
- Web servers, proxies, load balancers, API gateways, CDNs, service mesh.
- CI/CD, source control, IaC, config management, feature flags.
- Identity providers, SSO, secrets managers.
- Current monitoring, logging, alerting, incident, and ticketing tools (incumbents to replace or integrate).
- Third-party SaaS the prospect wants connected.

Details per item:

- **Languages**: capture name AND version (".NET 8", "Java 17"). If no version, add a version question to the Clarification Summary.
- **Frameworks**: capture framework AND version ("Spring Boot 3.2", "Next.js 14").
- **Infrastructure**: platform, version, configuration ("Kubernetes 1.28 on EKS").
- **Databases**: type and version ("PostgreSQL 15").
- **Rendering modes**: for frontend frameworks, capture SSR/CSR/SSG/ISR. If missing, add a question to the Clarification Summary (SSR needs server-side APM; CSR/SSG only needs Browser RUM).
- **Compilation and runtime modes**: NativeAOT, GraalVM native-image, Lambda SnapStart, Provisioned Concurrency. If missing and relevant, add a question to the Clarification Summary (these affect instrumentation).
- **One technology per row**: "Angular on web, mobile moving from Ionic to Swift" becomes three rows.
- **Version matters**: include it if given. If not, ask in the Clarification Summary; never assume one.

## Handling Ambiguous or Incomplete Requirements

- **Vague** ("need good monitoring"): create a row, "Clarification", one specific question.
- **Contradictory** ("fully on-premise" vs "cloud-first"): one row each, both "Clarification", conflict noted in the Clarification Summary.
- **Missing details** ("need Kubernetes support"): answer only what the source confirms for what is known, note what to confirm.
- **Out of scope** ("need a new CRM"): "Clarification", the one-sentence question confirms what they expect from Datadog.
- **Duplicates** from different sources: one row, quote both with attribution, conflicts go in the Clarification Summary.

## Important principles

- **Direct quotes over paraphrasing**, with attribution.
- **Gaps are valuable, fabrication is dangerous.** Ten honest Skipped or Clarification rows beat five plausible fabrications.
- **Surface contradictions.** Show both quotes; do not pick a side.
- **The template is the contract.** No extra, skipped, or reordered columns.
- **"Comply" is not "Yes".** Use Comply for compliance, legal, regulatory, and policy questions (SOC 2, ISO 27001, GDPR, FedRAMP, DPA). Never use Yes for these.
- **One requirement, one row.** Split React and React Native; split technical and compliance dimensions.
- **When in doubt about the prospect, Clarification. When in doubt about Datadog, Skipped.** Never over-claim.
- **Flag technical gaps proactively** in the Clarification Summary: missing version, rendering mode, or compilation mode.
- **Research is mandatory.** Ground every response in docs, GitHub, or OTel found via search, never training data alone.
- **One sentence per Response. Do not over-generate.**
