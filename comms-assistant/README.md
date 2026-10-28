# comms-assistant

Draft and summarise Slack communications and build a daily TIL FAQ newsletter using MCP tools.

## Prerequisites

Slack MCP tools must be available in your Claude Code environment. These are typically provided by a Slack MCP server plugin (e.g., `plugin-dev@claude-plugins-official`).

Required MCP tools:
- `slack_search_channels` — find channels by name
- `slack_read_channel` — read recent messages in a channel
- `slack_read_thread` — read a specific thread
- `slack_send_message` — deliver composed content to your own self-DM for review
- `slack_read_user_profile` — look up your own Slack user ID at runtime (used by `drafting-gmail`)

## Skills

### summarising-slack-channel

Summarise recent activity in one or more Slack channels into Q&A blocks with tags, then build a daily TIL FAQ newsletter from them. Start the agent in the folder where you want the files.

What it does:
1. Saves one summary file per channel, named `{section}-{channel}-{YYYY-MM-DD}-to-{YYYY-MM-DD}.md`.
2. Copies every Q&A block whose `TAGS:` match any newsletter tag into `newsletter-{today}.md`. The file is created or appended to. Blocks already in it are skipped.
3. Moves this run's summary files into `archive-{today}/`.

Default newsletter tags are `#new-feature #presentation #deadline`. Tags you supply replace the defaults. Blocks with a stated deadline are tagged `#deadline`.

**Example prompts:**
- "Summarise #general"
- "What happened in #engineering today?"
- "Catch me up on #announcements"
- "Summarise #example-support for the past 3 days, newsletter tags #apm #breaking-change"

### drafting-gmail

Draft an email from a structured template. There is no Gmail MCP, so the finished email (with a `Subject:` line) is sent to your own Slack self-DM after you confirm it, ready to copy and paste into Gmail. Templates live in `skills/drafting-gmail/references/`:
- `POC-STATUS-UPDATE-EMAIL-TEMPLATE.md`: PoC status updates and follow-ups after a meeting or call
- `DIRECT-EMAIL-TEMPLATE.md`: a direct email to a colleague, prospect or customer about a specific topic

To add a template, create a new file in `references/` with the same structure and add a row to the template table in `SKILL.md`.

**Note:** the skill only ever sends to your own Slack self-DM. Your Slack user ID is looked up from your Slack profile at runtime, so nothing personal is stored in this repo.

**Example prompts:**
- "Draft a PoC update email to ACME after today's call"
- "Write a follow-up email to my colleague about the trial timeline"
- "Compose a thank you email to the prospect for the workshop"
