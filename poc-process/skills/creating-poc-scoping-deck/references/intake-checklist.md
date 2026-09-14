# Intake Checklist

What the deck needs, grouped by slide, with what to do when the notes are silent.

The organising rule: **the notes are evidence, not a starting point for invention.**
Fill what they support, ask about what they do not, and leave a bracket standing for
anything still unanswered. A deck with visible `[Champion Name]` placeholders is
awkward. A deck confidently naming a champion nobody mentioned is a credibility
failure you will discover in front of the prospect.

Three-way split for every field below:

| Grounded | Derivable | Must ask |
|---|---|---|
| Stated in the notes. Use it. | Follows from what is stated — a use case implied by a named pain, a future state that is the stated pain resolved. Use it, and say so when you summarise. | Neither stated nor implied. Ask. If still unanswered, leave the bracket and log it in `open-questions.md`. |

## Slide 1 and 19 — Cover and Thank you

- Prospect / customer name, exactly as they write it
- Presentation date
- AE name; **SE name** (slide 1 has `Jek Bao Choo` hardcoded, slide 19 uses `[SE Name]`)

Usually in the meeting invite rather than the notes. Ask if absent — never guess a name.

## Slide 3 — Current & Future States

- Current state: the gaps and challenges, as a description plus supporting items
- Future state: the desired business outcomes, same shape

This has the highest discovery dependency of any slide. **Ground the current state
strictly in what the customer said.** The future state may be formulated — it is
normally the current-state pain resolved, expressed as a business outcome rather than a
product capability ("payments incidents triaged in one place" beats "Datadog Log
Management deployed").

If the notes describe pain only in tool terms ("Splunk is expensive"), ask what it
costs them operationally. A scoping deck that reflects tooling complaints back at the
prospect tells them nothing they did not already know.

## Slide 4 — Define Success Criteria

- 3 business use cases
- 3 success criteria

Criteria must be **testable within the PoC window**. "Improve observability" is not a
criterion; "a single query returns payments logs across all three AWS accounts" is.
Each criterion should pair with a use case and be something you could jointly mark
pass/fail on the final day.

If the notes yield fewer than three, say so rather than padding to three. Two real
criteria beat three where one is filler.

## Slide 5 — MTTD Calculation

Six inputs, two derived, two percentages:

| Field | Token | Source |
|---|---|---|
| Major incidents per year, before | `[99]` | customer |
| FTEs per incident, before | `5:[12]` (1st) | customer |
| Hours per incident, before | `[22]` | customer |
| Total hours per year, before | `[19,000]` | multiply the three |
| Major incidents per year, with Datadog | `[72]` | modelled |
| FTEs per incident, with Datadog | `5:[12]` (2nd) | usually unchanged |
| Hours per incident, with Datadog | `5:[12]` (3rd) | modelled |
| Total hours per year, with Datadog | `[10,368]` | multiply the three |
| % reduction | `[45]` ×2 | derive |

**This is one of the two slides discovery notes almost never cover.** Incident counts
and hours per incident come from the customer's own incident record, not from you. Ask
for them. If they are not available, leave the whole slide bracketed and flag it —
a fabricated ROI number that a prospect later disproves costs more than a blank slide,
and the modelled "with Datadog" figures only carry weight if the "before" ones are the
customer's own.

Check the arithmetic multiplies out before packing.

## Slide 6 and 17 — Meeting Cadence

- Frequency (template default: 2x per week)
- Specific date and time for the recurring slot
- Communication channel: Slack or Teams, and who sets up the shared channel
- Showback meeting: audience and date

Slide 17 repeats slide 6 minus the showback block. Keep them consistent.

## Slide 7 — Roles and responsibilities

- Prospect name for the Venn label
- Whether the stated Datadog and prospect responsibilities need amending

The two `Notes` callouts are deliberately blank for live annotation. Leave them.

## Slide 8 — Contacts

Datadog side: AE and SE, each with title, phone, email.
Prospect side: Champion, DevOps Engineer, SRE, each with name, title, phone, email.

**The second slide discovery notes rarely cover.** Phone numbers in particular are
almost never in meeting notes. Ask for what you can, and leave the rest bracketed
rather than inventing.

Note the champion's title is hardcoded as `VP of Engineering` — confirm or replace.
Anchor the repeated `[email]` and `[phone number]` tokens; see `slide-map.md`.

## Slides 10, 12, 15 — Datadog site

Which Datadog site the prospect will use. This drives every URL on these three slides,
and the deck ships pointing at US1.

| Site | URL | Cloud |
|---|---|---|
| US1 (East) | `https://app.datadoghq.com/` | AWS |
| US3 (West) | `https://us3.datadoghq.com/` | Azure |
| US5 (Central) | `https://us5.datadoghq.com/` | GCP |
| EU1 | `https://app.datadoghq.eu/` | GCP |
| AP1 | `https://ap1.datadoghq.com/` | AWS |

Data residency requirements usually decide this, so ask about those too if the region
is unstated. Also ask whether RUM is in scope — if not, drop slide 13.

## Slide 18 — Next steps

- Target PoC kick-off date
- Prerequisites specific to this prospect (firewall rules, proxy, IAM roles, agent
  deployment approval, change-freeze windows)

## Added slides — tech stack and timeline

Only build these when the notes support them; see SKILL.md Step 6.

**Tech stack / environment** — languages and frameworks *with versions*, OS, databases,
cloud services, log sources, orchestration, plus which environment the PoC runs in
(pre-prod vs prod), its size, and who owns it. Versions matter because they decide
agent and tracer compatibility, and "Java" without "17" is not actionable.

**Timeline** — start date, kick-off, checkpoints, showback, decision date. If the notes
have no dates at all, skip the slide rather than inventing a schedule; slide 18 already
drives to the MAP, which is where dates properly belong.

## How to ask

Use `AskUserQuestion` when it is available; otherwise ask conversationally. Ask only
what is genuinely missing — re-asking something the notes already answer reads as not
having read them.

Batch the questions. One round of eight grouped questions respects the user's time far
more than eight separate exchanges, and they can see the whole shape of what is missing
at once. Lead with the two that block the most slides: the MTTD inputs and the contact
roster.
