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
