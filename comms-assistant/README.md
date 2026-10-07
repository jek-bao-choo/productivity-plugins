# comms-assistant

Draft and summarise Slack communications using MCP tools.

## Prerequisites

Slack MCP tools must be available in your Claude Code environment. These are typically provided by a Slack MCP server plugin (e.g., `plugin-dev@claude-plugins-official`).

Required MCP tools:
- `slack_search_channels` — find channels by name
- `slack_read_channel` — read recent messages in a channel
- `slack_read_thread` — read a specific thread
- `slack_send_message` — deliver composed content to your own self-DM for review

## Skills

### summarising-slack-channel

Summarise recent activity in a Slack channel. Produces a structured summary with key highlights, discussion topics, action items, and questions awaiting response.

**Example prompts:**
- "Summarise #general"
- "What happened in #engineering today?"
- "Catch me up on #announcements"

### drafting-gmail

Draft an email from a structured template. There is no Gmail MCP, so the finished email (with a `Subject:` line) is sent to your own Slack self-DM after you confirm it, ready to copy and paste into Gmail. Templates live in `skills/drafting-gmail/references/`:
- `POC-STATUS-UPDATE-EMAIL-TEMPLATE.md`: PoC status updates and follow-ups after a meeting or call
- `DIRECT-EMAIL-TEMPLATE.md`: a direct email to a colleague, prospect or customer about a specific topic

To add a template, create a new file in `references/` with the same structure and add a row to the template table in `SKILL.md`.

**Note:** the skill only ever sends to a hardcoded Slack user ID (`U093Q9Z3SKU`). Change it in `SKILL.md` before using the skill under another Slack account.

**Example prompts:**
- "Draft a PoC update email to ACME after today's call"
- "Write a follow-up email to my colleague about the trial timeline"
- "Compose a thank you email to the prospect for the workshop"
