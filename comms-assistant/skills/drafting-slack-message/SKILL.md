---
name: drafting-slack-message
description: >-
  This skill should be used when the user wants to draft a Slack message without sending
  it immediately. It applies when the user says "draft a reply to the thread in #channel",
  "compose a message for #announcements", "help me write a response to {person}",
  "prepare a message for the team channel", or "draft a follow-up in #project-updates".
  It also applies when the user mentions drafting, composing, writing, or preparing a
  Slack message — even if they don't explicitly say "draft". IMPORTANT: This skill
  creates drafts only. It must NEVER send a message directly. Always use
  slack_send_message_draft, never slack_send_message.
version: "0.1.0"
author: productivity-plugins
tags: slack, draft, message, compose, reply
---

# Slack Message Drafting

Draft a Slack message or thread reply without sending it. The draft is saved to Slack for the user to review and send manually.

## Critical Constraint

**This skill MUST only create drafts using `slack_send_message_draft`. It MUST NEVER use `slack_send_message` to send messages directly.** The user must review and send drafts manually from Slack.

## Prerequisites

The following Slack MCP tools must be available:
- `slack_search_channels`
- `slack_read_channel`
- `slack_read_thread`
- `slack_send_message_draft`

## Workflow

### Step 1 — Understand the context

Determine what the user wants to say, to whom, and in which channel or thread.

- If the user references a specific conversation, note the channel and thread details.
- If the intent is unclear, ask the user to clarify the target channel and message purpose.

### Step 2 — Find the target channel

Use `slack_search_channels` to resolve the channel ID from the channel name.

- If multiple matches, present them and ask the user to confirm.

### Step 3 — Read relevant context (if replying)

If drafting a thread reply:
- Use `slack_read_thread` with the parent message timestamp to understand the full thread.

If drafting a new message:
- Use `slack_read_channel` to understand recent channel context and tone.

### Step 4 — Compose the draft

Write the message content following the review format in `references/DRAFT-MESSAGE-TEMPLATE.md`.

- Match the tone and style of the channel.
- Use Slack mrkdwn formatting (bold, lists, links, mentions).
- Keep the message concise and clear.

### Step 5 — Confirm with user

Present the composed draft to the user for review before saving. Show:
- The target channel and thread (if applicable)
- The full draft content
- A checklist for review

Iterate until the user is satisfied with the draft.

### Step 6 — Save as draft

Use `slack_send_message_draft` with:
- `channel_id` — the resolved channel ID
- `message` — the confirmed draft content
- `thread_ts` — the parent message timestamp (only for thread replies)

Report the Slack web client URL so the user can find their draft in **Drafts & Sent**.

## Output Format

Follow the review format in `references/DRAFT-MESSAGE-TEMPLATE.md` when presenting drafts to the user.

## Scope Guardrails

- **NEVER use `slack_send_message`** — only `slack_send_message_draft`.
- Always present the draft to the user and get confirmation before saving.
- If a draft already exists for that channel, inform the user (Slack allows only one attached draft per channel).
- Cannot draft in externally shared (Slack Connect) channels.

## Failure Handling

- **Channel not found**: Suggest searching with `slack_search_channels` using alternative terms.
- **Draft already exists**: Inform the user they have an existing draft in that channel that must be sent or deleted first.
- **Externally shared channel**: Inform the user that drafts cannot be created in Slack Connect channels.
