---
name: drafting-slack-message
description: >-
  This skill should be used when the user wants to draft a Slack message using a
  specific template. It applies when the user says "draft a PoC status update",
  "write a status update from my sales notes", "update the team on PoC progress",
  "draft a message to [colleague]", "write a DM to [person]", or "message [name]
  about...". It also applies when the user mentions drafting, composing, writing,
  or preparing a Slack message — even if they don't explicitly say "draft". This
  skill supports multiple message templates (PoC status updates, colleague DMs, and
  more in the future). All messages are sent to the user's own Slack DM for manual
  copy-paste to the intended destination. IMPORTANT: This skill must NEVER send
  messages to anyone other than the user themselves. Always use slack_send_message
  with channel_id U093Q9Z3SKU (the user's own DM).
version: "0.2.0"
author: productivity-plugins
tags: slack, draft, message, compose, template, poc, status, dm
---

# Slack Message Drafting (Template-Based)

Draft a Slack message using a structured template. All drafts are sent to the user's own Slack DM (Jek Bao Choo) so the user can review, copy, and paste to the intended channel or person.

## Critical Constraints

- **NEVER send messages to anyone other than the user.** Always use channel_id `U093Q9Z3SKU` (Jek Bao Choo's user ID) when calling `slack_send_message`. The user will copy-paste the message from their self-chat to the intended destination.
- **NEVER use `slack_send_message` with any channel_id other than `U093Q9Z3SKU`.**

## Prerequisites

The following Slack MCP tools must be available:
- `slack_send_message` — to send the composed message to the user's self-DM

## Workflow

### Step 1 — Determine the template

Based on the user's request, select the appropriate template:

| User intent | Template |
|---|---|
| PoC update, status update, sales notes, proof of concept, team update, customer/prospect meeting notes | `references/POC-STATUS-UPDATE-TEMPLATE.md` |
| Message to a colleague, DM, direct message, writing to a specific person | `references/COLLEAGUE-DM-TEMPLATE.md` |

If the intent is ambiguous, ask the user which type of message they want to draft.

> **Adding new templates:** Create a new file in `references/` following the same structure (Purpose, Input Required, Message Format, Rules, Checklist) and add a row to the table above.

### Step 2 — Gather input

Read the selected template file from `references/` to understand the required inputs and format.

Collect the information needed for the selected template:

- **PoC Status Update**: Accept the user's sales notes. Determine the communication mode (Zoom / Ms Teams / Email) and date — infer from the notes if possible, otherwise ask.
- **Colleague DM**: Determine the colleague's name and the message intent — ask if not already clear from the user's request.

### Step 3 — Compose the draft

Format the message strictly according to the selected template:

- For **PoC Status Update**: Extract attendees, achievements, blockers, and next steps from the sales notes. Summarize concisely. Do not fabricate information — only use what can be inferred from the provided notes.
- For **Colleague DM**: Draft a message that starts with "Hi", is friendly yet professional, short and warm.

Use Slack mrkdwn formatting throughout. Avoid using " — " or " - " to connect clauses within sentences. These dash patterns are a telltale sign of AI-generated writing. Write short, direct sentences instead.

### Step 4 — Confirm with user

Present the composed draft for review. Show:
- Which template was used
- The full draft content formatted as it will appear in Slack
- A reminder that it will be sent to the user's own Slack DM

Iterate until the user is satisfied with the draft.

### Step 5 — Send to self-DM

Use `slack_send_message` with:
- `channel_id`: `U093Q9Z3SKU`
- `message`: the confirmed draft content

After sending, share the message link and remind the user: "Message sent to your self-DM. Copy and paste it to the intended destination."

## Output Format

Follow the template file selected in Step 1. See the `references/` directory for all available templates:
- `references/POC-STATUS-UPDATE-TEMPLATE.md` — PoC status update for internal team
- `references/COLLEAGUE-DM-TEMPLATE.md` — Direct message to a colleague

## Scope Guardrails

- **NEVER send to anyone other than self** — only use channel_id `U093Q9Z3SKU` with `slack_send_message`.
- Always present the draft to the user and get confirmation before sending.
- Every draft must match a known template. If the user's request doesn't match any template, ask for clarification.

## Failure Handling

- **No matching template**: Ask the user which template type fits their needs, or whether they'd like to describe a new template format.
