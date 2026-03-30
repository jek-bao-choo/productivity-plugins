---
name: drafting-gmail
description: >-
  This skill should be used when the user wants to draft an email or Gmail message.
  It applies when the user says "draft an email to [person]", "write a follow-up
  email after the meeting", "compose a PoC update email", "email [prospect] about
  the status", "draft a thank you email", "write an email to my colleague", or
  "prepare an email for [customer]". It also applies when the user mentions drafting,
  composing, writing, or preparing an email, even if they don't explicitly say "Gmail"
  or "email". This skill supports multiple email templates (PoC status update emails,
  direct emails, and more in the future). Since no Gmail MCP is available, the composed
  email is sent to the user's Slack self-DM for copy-paste into Gmail.
version: "0.1.0"
author: productivity-plugins
tags: gmail, email, draft, compose, poc, status, follow-up
---

# Gmail Email Drafting (Template-Based)

Compose an email using a structured template. Since no Gmail MCP is available, the finished email is sent to the user's Slack self-DM (Jek Bao Choo) for copy-paste into Gmail.

## Critical Constraints

- **NEVER send to anyone other than the user.** Always use channel_id `U093Q9Z3SKU` (Jek Bao Choo's user ID) when calling `slack_send_message`.
- **NEVER use `slack_send_message` with any channel_id other than `U093Q9Z3SKU`.**

## Prerequisites

The following Slack MCP tools must be available:
- `slack_send_message` — to deliver the composed email to the user's self-DM

## Workflow

### Step 1 — Determine the template

Based on the user's request, select the appropriate template:

| User intent | Template |
|---|---|
| PoC update email, follow-up email after meeting/call, status update to prospect/customer | `references/POC-STATUS-UPDATE-EMAIL-TEMPLATE.md` |
| Direct email to a colleague, prospect, or customer about a specific topic | `references/DIRECT-EMAIL-TEMPLATE.md` |

If the intent is ambiguous, ask the user which type of email they want to draft.

> **Adding new templates:** Create a new file in `references/` following the same structure (Purpose, Input Required, Email Format, Rules, Checklist) and add a row to the table above.

### Step 2 — Gather input

Read the selected template file from `references/` to understand the required inputs and format.

Collect the information needed for the selected template:

- **PoC Status Update Email**: Accept the user's sales notes. Determine the communication mode (Zoom / Ms Teams / In-Person) and date. Infer from the notes if possible, otherwise ask.
- **Direct Email**: Determine the recipient's name and the message intent. Ask if not already clear from the user's request.

### Step 3 — Compose the email

Format the email strictly according to the selected template. Always include a `Subject:` line at the top.

- For **PoC Status Update Email**: Extract attendees, achievements, and next steps from the sales notes. Summarize concisely. Do not fabricate information. This is a client-facing email so maintain a professional, polished tone.
- For **Direct Email**: Draft a message that starts with "Hi", "Hello", or "Dear" as appropriate. Friendly yet professional, short and warm.

Avoid using " — " or " - " to connect clauses within sentences. These dash patterns are a telltale sign of AI-generated writing. Write short, direct sentences instead.

### Step 4 — Confirm with user

Present the composed email for review. Show:
- Which template was used
- The full email content including subject line
- A reminder that it will be sent to the user's Slack self-DM for copy-paste into Gmail

Iterate until the user is satisfied with the email.

### Step 5 — Send to Slack self-DM

Use `slack_send_message` with:
- `channel_id`: `U093Q9Z3SKU`
- `message`: the confirmed email content (including the Subject line)

After sending, share the message link and remind the user: "Email sent to your Slack self-DM. Copy and paste it into Gmail."

## Output Format

Follow the template file selected in Step 1. See the `references/` directory for all available templates:
- `references/POC-STATUS-UPDATE-EMAIL-TEMPLATE.md` — PoC status update email for prospects/customers
- `references/DIRECT-EMAIL-TEMPLATE.md` — Direct email to a colleague, prospect, or customer

## Scope Guardrails

- **NEVER send to anyone other than self** — only use channel_id `U093Q9Z3SKU` with `slack_send_message`.
- Always present the email to the user and get confirmation before sending.
- Every email must match a known template. If the user's request doesn't match any template, ask for clarification.
- Always include a subject line in the output.

## Failure Handling

- **No matching template**: Ask the user which template type fits their needs, or whether they'd like to describe a new template format.
