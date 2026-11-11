# comms-assistant

Draft and summarise Slack communications, build a daily TIL FAQ newsletter, refine questions for Slack with a recommended channel, and flatten communication with people across Slack, Gmail, Calendar, Drive and Zoom using MCP tools.

## Prerequisites

Slack MCP tools must be available in your Claude Code environment. These are typically provided by a Slack MCP server plugin (e.g., `plugin-dev@claude-plugins-official`).

Required MCP tools:
- `slack_search_channels` — find channels by name (also used by `refining-question-for-slack` to recommend a channel)
- `slack_read_channel` — read recent messages in a channel
- `slack_read_thread` — read a specific thread
- `slack_send_message` — deliver composed content to your own self-DM for review
- `slack_read_user_profile` — look up your own Slack user ID at runtime (used by `drafting-gmail`, `flattening-communication` and `refining-question-for-slack`)
- `slack_search_public_and_private` (or `slack_search_public`) and `slack_search_users` — search messages and resolve people (used by `flattening-communication`; message search is also used by `refining-question-for-slack`)

`flattening-communication` also uses Gmail, Google Calendar, Google Drive and Zoom MCPs when available. Without them it runs on Slack only and reports the gap.

## Skills

Every skill runs only when you type its slash command (for example `/drafting-gmail`). Claude never starts them on its own.

### summarising-slack-channel

Summarise recent activity in one or more Slack channels into Q&A blocks with tags, then build a daily TIL FAQ newsletter from them. Start the agent in the folder where you want the files.

What it does:
1. Saves one summary file per channel, named `{section}-{channel}-{YYYY-MM-DD}-to-{YYYY-MM-DD}.md`.
2. Copies every Q&A block whose `TAGS:` match any newsletter tag, or whose `MESSAGE_COUNT` is more than 10, into `newsletter-{today}.md`. The file is created or appended to. Blocks already in it are skipped.
3. Moves this run's summary files into `archive-{today}/`.

Default newsletter tags are `#new-feature #presentation #deadline`. Tags you supply replace the defaults. Blocks with a stated deadline are tagged `#deadline`.

**Example prompts:**
- `/summarising-slack-channel #general`
- `/summarising-slack-channel #engineering today`
- `/summarising-slack-channel #example-support for the past 3 days, newsletter tags #apm #breaking-change`

### flattening-communication

See what each person in a table is involved in (accounts, opportunities, projects, meetings and discussions across the workspace, not only with you) and how they are behaving. Each run writes a short, readable `analysis-{display-name}-{YYYY-MM-DD}.md` report per person. Start the agent in the folder where you want the files.

Input table:

```markdown
| SLACK_USER_ID | SLACK_DISPLAY_NAME | EMAIL_ADDRESS |
```

What it does:
1. Runs every Slack search type per person (from:, with:, mentions, is:thread, in:@ DM, is:dm, creator: files, reactions, saved), searches your Gmail by their address, reads their calendar (or the meetings you share with them), lists the Google Drive files they own or last edited that you can see (newest first, in a **Drive files** section, for the same timeframe as the report, optionally filtered by name keyword and type doc/sheet/slides/pdf), and pulls their Zoom meetings (with AI summaries and next steps), chats, canvases, notes and calls.
2. Removes duplicates within the run.
3. Writes `analysis-{display-name}-{YYYY-MM-DD}.md` for each person, named with the date it runs. A rerun on the same day replaces that day's file. Each report has a **Summary** (what they are involved in, mood, character, meetings, watch out, follow up), **Involved in** blocks grouped by account or project, and a one-line-per-item **Timeline**. Every involvement ends with **Sources** links such as `#channel-name · Thu 29 Oct 11:43`. Involvement blocks also list stated decisions, action items and open questions, each with its source. Character, behaviour and sentiment come only from the person's own words. Behaviour labels such as complaining or blaming always carry a quote.

Default timeframe is 00:00 GMT+8 yesterday until now, or from Friday 00:00 when run on a Monday. It is built for a daily Monday to Friday schedule. Meetings are included up to 23:59 today, so you also see what is still coming up. Any period you supply overrides it. Slack, Gmail and Drive only cover what your own account can see. Drive records only the last editor of a file.

**Example prompts:**
- `/flattening-communication people.md`
- `/flattening-communication` (then paste the table)
- `/flattening-communication people.md for the past week, Drive files: type sheet, name contains pipeline`

### refining-question-for-slack

Refine rough question text so you can post it in a company Slack channel and get clear, relevant answers, with one recommended channel per question. It runs only when you type `/refining-question-for-slack`; Claude never picks it up on its own. Paste the text with the command or in your next message.

What it does:
1. Splits the text into distinct questions. Each becomes one sentence starting with `Hi,` and `Can`, `Does`, `What`, `When`, `Where`, `Why`, `Who` or `How`, with a standalone `Context:` block. Grammar is fixed, technical details and uncertainty are kept, nothing is invented and the questions are not answered.
2. Searches Slack channels and messages to recommend one primary channel per question, with a link when the tools return one and a short reason. If no channel can be verified it says so instead of guessing.
3. Returns each block as:

```
Hi, [refined question]?

Context: [relevant background information]

Recommended Slack channel: [#channel-name and link] — [brief reason]
```

4. Sends each block to your own Slack self-DM so it is easy to copy. Your user ID is looked up from your Slack profile at runtime. The skill never posts to a channel or anyone else.

**Example prompts:**
- `/refining-question-for-slack` (then paste the text in your next message)
- `/refining-question-for-slack does the java tracer support log injection without a restart...`

### drafting-gmail

Draft an email from a structured template. There is no Gmail MCP, so the finished email (with a `Subject:` line) is sent to your own Slack self-DM after you confirm it, ready to copy and paste into Gmail. Templates live in `skills/drafting-gmail/references/`:
- `POC-STATUS-UPDATE-EMAIL-TEMPLATE.md`: PoC status updates and follow-ups after a meeting or call
- `DIRECT-EMAIL-TEMPLATE.md`: a direct email to a colleague, prospect or customer about a specific topic

To add a template, create a new file in `references/` with the same structure and add a row to the template table in `SKILL.md`.

**Note:** the skill only ever sends to your own Slack self-DM. Your Slack user ID is looked up from your Slack profile at runtime, so nothing personal is stored in this repo.

**Example prompts:**
- `/drafting-gmail PoC update email to ACME after today's call`
- `/drafting-gmail follow-up email to my colleague about the trial timeline`
- `/drafting-gmail thank you email to the prospect for the workshop`
