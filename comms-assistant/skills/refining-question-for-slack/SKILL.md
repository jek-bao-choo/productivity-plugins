---
name: refining-question-for-slack
description: >-
  Refine rough question text into standalone one-sentence Slack questions that start
  with "Hi," plus a Context block, recommend one verified Slack channel per question,
  and send the result only to the user's own Slack self-DM. Run only when the user
  explicitly types /refining-question-for-slack.
disable-model-invocation: true
version: "0.2.0"
author: productivity-plugins
tags: slack, question, refine, rewrite, channel, recommend, ask
---

# Refining Questions for Slack

Turn rough question text into clear, standalone Slack questions that get fast, relevant answers, and recommend the best channel for each one. People in busy channels skim. A question that is one clear sentence, with its background underneath, gets answered; a paragraph with three tangled questions gets ignored or half answered. That is the reason for every formatting rule below.

## Critical Constraints

- **Send only to the user's own self-DM.** `slack_send_message` may be called only with `channel_id` set to the signed in user's own Slack user ID, looked up at runtime with `slack_read_user_profile` (Step 6). Never send to a channel, another person, a group DM, or a thread. Never call any other Slack write tool. The user posts the questions themselves.
- **Never hardcode a Slack user ID** in this skill. It lives in a public repo.
- **Do not answer the questions.** The goal is a better question, not a reply. Even if you know the answer, leave it out.
- **Do not invent information.** No made up facts, versions, channel names, or links.

## Prerequisites

Slack MCP tools, when connected:
- `slack_search_channels`: find candidate channels by keyword
- `slack_search_public_and_private` (or `slack_search_public`): find where similar questions were asked and answered
- `slack_read_user_profile`: look up the signed in user's own Slack user ID
- `slack_send_message`: deliver the result to the user's self-DM only

Without Slack tools the skill still refines the text, says the channel could not be verified, and leaves the output in chat.

## Workflow

### Step 1: Get the text

If the user invoked the skill without the text to refine, reply in one short line that you are ready for the text, then wait. Do not search Slack, guess at a topic, or produce sample output until the text arrives.

### Step 2: Extract each distinct question

Read the whole text and list every distinct thing the user wants to know. Questions are often hidden in statements ("not sure whether X works with Y", "wondering about the timeline"). Split compound questions ("Does X support Y and how do I enable it?") into separate questions. Never nest one question inside another.

For each question, note which parts of the background it actually needs. Shared background goes into every block that needs it, because each block will be posted on its own.

### Step 3: Refine each question

Write each question as **one sentence** that starts with `Hi,` followed by `Can`, `Does`, `What`, `When`, `Where`, `Why`, `Who`, or `How`, whichever fits naturally.

- Fix grammar and improve clarity while keeping the user's meaning and intent. If the user asks "is it possible", keep it a "Can" or "Does" question; do not turn it into a "How" question that assumes the answer is yes.
- Keep it concise, professional, and natural, the way a thoughtful colleague would write it.
- Put essential context in the question itself only when the question is unclear without it (for example the product, feature, or environment). Everything else goes under `Context:`.
- Under `Context:` put the supporting background: what the user is trying to do, what they tried, versions, environment, constraints, deadlines. Do not repeat what the question already says.
- Keep technical details exactly as given (names, versions, error text, config keys). Keep uncertainty too. If the user says "I think" or "not sure if", the context should say so rather than state it as fact. Responders need to know what is confirmed and what is a guess.
- Avoid " — " or " - " joining clauses in the text meant for posting. Use short sentences or commas instead. These dash patterns read as AI generated.
- If there is genuinely no background beyond the question, write `Context: None beyond the question.` rather than padding.

### Step 4: Find the best channel for each question

Use whichever Slack search tools are connected:

1. `slack_search_channels` with 2 to 4 topic keywords from the question (product, feature, team, function). Try a couple of keyword variants if the first search is thin.
2. `slack_search_public_and_private` (or `slack_search_public`) with the key terms to see where similar questions were asked and actually answered.

Judge candidates by the channel's description or purpose, its intended audience (for example a support or help channel versus an announcements or team-only channel), and whether relevant discussions happen there recently. Prefer channels meant for questions over announcement or alert channels. Recommend **one** primary channel per question with a brief reason grounded in what you found (its purpose, or that similar questions get answered there).

For the link, use a permalink or workspace URL returned by the tools, or build `https://<workspace>.slack.com/archives/<CHANNEL_ID>` only when both the workspace domain and channel ID came from tool results. Otherwise give the channel name without a link.

If no suitable channel can be verified, or Slack tools are not available, say so plainly in the recommendation line, for example `Recommended Slack channel: Could not verify a suitable channel (Slack search tools are not connected).` Never guess a channel name.

### Step 5: Return the result

Return only the refined blocks, one per question, in this exact format, separated by `---` when there is more than one:

```
Hi, [refined question]?

Context: [relevant background information]

Recommended Slack channel: [#channel-name and link] — [brief reason]
```

No preamble, no commentary, no answers. The first two parts are the text to post. The recommendation line is for the user only and stays separate from it.

### Step 6: Send to the self-DM

Call `slack_read_user_profile` with no `user_id` to get the signed in user's own profile, and take the user ID from it. Do not guess or reuse an ID from anywhere else.

Then call `slack_send_message` once per question block with:
- `channel_id`: the user ID from the profile lookup, and nothing else
- `message`: that block exactly as shown in Step 5

One message per block makes each question easy to copy. After sending, add one line listing the message links. If the profile lookup or send fails, or the tools are missing, keep the output in chat and say it was not sent.

## Examples

**Example 1: several questions hidden in one paragraph**

Input:
> hey so we're running the java tracer on k8s, i think version 1.30ish, and traces show up but no logs are linked to them. does log injection need to be turned on separately? also is there a way to do it without restarting pods cause the customer has a change freeze until friday. and who owns the java tracer docs because the page seems out of date

Output:
```
Hi, Does trace and log correlation for the Java tracer need log injection enabled separately?

Context: We run the Java tracer on Kubernetes, I think around version 1.30. Traces show up, but no logs are linked to them.

Recommended Slack channel: #example-apm-java — Channel purpose is Java tracer questions, and recent threads there cover log injection.

---

Hi, Can log injection be enabled for the Java tracer on Kubernetes without restarting pods?

Context: We run the Java tracer on Kubernetes, I think around version 1.30, and need log injection so logs link to traces. The customer has a change freeze until Friday, so restarting pods is not an option before then.

Recommended Slack channel: #example-apm-java — Same audience, and the question depends on Java tracer configuration behaviour.

---

Hi, Who owns the Java tracer documentation?

Context: The Java tracer log injection page seems out of date, and I would like to flag it to the right team.

Recommended Slack channel: #example-docs — Channel description says it is for documentation feedback and ownership questions.
```

**Example 2: preserving uncertainty**

Input:
> not sure if this is right but i think the agent drops custom metrics over some limit? when is that applied

Output:
```
Hi, When does the Agent apply a limit that drops custom metrics?

Context: I think the Agent drops custom metrics above some limit, but I am not sure this is correct.

Recommended Slack channel: Could not verify a suitable channel — No channel found whose purpose or recent discussions match Agent custom metric limits.
```

The channel names above are placeholders. Real recommendations must come from search results.

## Failure Handling

- **No question in the text:** ask the user what they want to find out.
- **Intent is ambiguous:** keep the user's uncertainty in the Context rather than picking an interpretation. If two readings lead to very different questions, ask which they mean.
- **Slack tools unavailable:** still refine every question, state that the channel could not be verified, and say the result was not sent to the self-DM.
