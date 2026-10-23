# comms-assistant

Draft and summarise Slack communications using MCP tools.

## Prerequisites

Slack MCP tools must be available in your Claude Code environment. These are typically provided by a Slack MCP server plugin (e.g., `plugin-dev@claude-plugins-official`).

Required MCP tools:
- `slack_search_channels` — find channels by name
- `slack_read_channel` — read recent messages in a channel
- `slack_read_thread` — read a specific thread
- `slack_send_message` — deliver composed content to your own self-DM for review
- `slack_read_user_profile` — look up your own Slack user ID and email at runtime (used by `extracting-til-faq-by-tags`)

`extracting-til-faq-by-tags` also needs a Gmail MCP plugin with a send email tool.

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

**Note:** the skill only ever sends to your own Slack self-DM. Your Slack user ID is looked up from your Slack profile at runtime, so nothing personal is stored in this repo.

**Example prompts:**
- "Draft a PoC update email to ACME after today's call"
- "Write a follow-up email to my colleague about the trial timeline"
- "Compose a thank you email to the prospect for the workshop"

### extracting-til-faq-by-tags

Build a daily FAQ newsletter from the summary files that `summarising-slack-channel` saves. Start the agent in the folder that holds those files. The skill only reads top level files named `{section}-{channel}-{YYYY-MM-DD}-to-{YYYY-MM-DD}.md` and never enters `archive*` folders.

What it does:
1. Copies every Q&A block whose `TAGS:` match any requested tag, or whose `DEADLINE:` is not `NONE`, into `newsletter-{today}.md`. The file is created or appended to. Blocks already in it are skipped.
2. Moves every scanned summary file into `archive-{today}/`.
3. Emails the newly added blocks to you with Gmail and sends them to your Slack self-DM. Your email and Slack user ID are looked up from your Slack profile at runtime, so nothing personal is stored in this repo.

Default tags are `#presentation #spreadsheet #new-feature`. Tags you supply replace the defaults.

**Example prompts:**
- "Extract my TIL FAQ"
- "Build today's newsletter from my TIL files"
- "Extract FAQ by tags #apm #breaking-change"
