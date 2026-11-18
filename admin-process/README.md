# admin-process

Admin process tools for timesheets, in three steps you control:

1. `/creating-daily-timesheet` builds the day's timesheet from your real activity as a Word document. It never submits anything.
2. You open the document, check the yellow rows, edit and save it.
3. `/submitting-timesheet-to-homerun` submits the reviewed document to Homerun, only after showing you exactly what will be sent and getting your yes.

## Prerequisites

`creating-daily-timesheet` reads from these MCP servers when they are connected. It never writes to any of them.

- **Google Calendar** (a Google Calendar or Google Workspace MCP): meetings, the backbone of the timesheet
- **Claude activity** (the `trajectory` MCP, which records AI coding agent sessions locally): Claude Code and Claude desktop sessions, plus Codex and Cursor if you use them, with real start and end times
- **Slack** (`slack_read_user_profile`, `slack_search_public_and_private` or `slack_search_public`): messages you sent
- **Gmail** (a Gmail MCP): emails you sent
- **Google Drive** (a Google Workspace or Drive MCP): files you edited

If a source is missing or not signed in, the skill carries on without it and says so in the document's notes. Python 3 is needed to build the .docx; no extra packages are required.

## Skills

### creating-daily-timesheet

Builds a gapless timesheet for a weekday from 08:00 to 19:00 in 30 minute blocks, with a one hour lunch around 12:00 (moved if a meeting sits there), and saves it as `timesheet-YYYY-MM-DD.docx` in the folder you run it from.

What it does:
1. Collects meetings from Calendar, AI sessions from trajectory, sent Slack messages, sent emails and Drive files you edited, for the day.
2. Places meetings (snapped to the half hour), leave and personal appointments first, then lunch, then observed work, merging activity into rows by account and kind of work.
3. Fills every remaining gap with a **proposed** row in a fixed order: your own calendar focus blocks, follow up after an account meeting, prep before one, work on a Drive file you edited, then start of day and inbox triage. Proposed rows are shaded yellow and carry a reason of a few words.
4. Tags each row with an **account**, inferred from external attendee and recipient domains, account Slack channels, and company names in titles, subjects, file names and Claude prompts. Accounts tied from a name only are listed in the chat reply for you to confirm. **Opportunity** is filled only from your opportunity list, never guessed.
5. Gives each row one of the 20 **Homerun types**, spelled exactly as Homerun shows them. Customer meetings become Discovery, Demo / New Business, Deal Progression or Post Sales Meeting by opportunity stage (from your list, else from words in the meeting title, else Deal Progression for you to confirm). PoC and trial work is Evaluation Work; non-eval prep and follow up is Customer Related Prep / Follow Up / Internal Meetings. The full type guide is in the skill's SKILL.md.
6. Writes a one page, landscape Word document: a summary line, the timesheet table (Start, End, Hours, Activity, Account, Opportunity, Type, Source), hours by account, and up to a few notes. Hours are decimal (0.5, 1.5) so they can go straight into Homerun.

It never overwrites an existing timesheet without asking, because you may have edited it. A date range writes one document per weekday, clipped at today. Run for today before 19:00, time after now shows only booked meetings, lunch and `Not yet worked`. Activity before 08:00 or after 19:00 is mentioned in the notes, not placed.

Lunch, personal appointments, leave and time not yet worked appear as rows of type `Lunch`, `Personal`, `Leave` and `Not yet worked` so the day stays gapless. They are not Homerun types; leave them out when submitting.

The skill's SKILL.md ends with a worked example of a full sample day.

**Everything is in SKILL.md.** Each skill is a single SKILL.md file. The small Python builder that writes and reads the .docx (standard library only, nothing to install) sits in an appendix at the end of `creating-daily-timesheet/SKILL.md`; Claude copies it to a temp folder when it runs. The submit skill uses the same appendix to read your edited document back and check it still runs 08:00 to 19:00 in half hour blocks with matching hours.

**Optional opportunity list.** To fill the Opportunity column, make meeting types exact, and keep account and opportunity names matching Homerun, create `opportunities.md` in your working folder (or `~/.claude/admin-process/opportunities.md`). Keep it private; it is ignored by git in this repo.

```markdown
| Account | Opportunity | Stage | Aliases | Domains | Slack channels |
|---|---|---|---|---|---|
| Acme | Acme FY27 Observability | 3 | ACME Corp | acme.com | #opp-acme, #ext-acme |
| Initech | | Closed won | | initech.com | #initech-support |
```

Account and Opportunity are copied exactly, so use the names Homerun shows. Stage is `Pre-opp`, `1`, `2`, `3`, `4`, `5` or `Closed won`. Only Account is required.

**Example prompts:**
- `/creating-daily-timesheet`
- `/creating-daily-timesheet yesterday`
- `/creating-daily-timesheet 16 to 20 Nov`
- `fill in my timesheet for last Friday`
- `how many hours did I spend on each opportunity this week?`

### submitting-timesheet-to-homerun

Submits a reviewed `timesheet-YYYY-MM-DD.docx` to Homerun through the Homerun MCP server. It runs only when you type the command, never on its own and never straight after the timesheet is built.

Before anything is sent it:
1. Reads the table back from the document, so your edits are what gets submitted, and stops if the edits broke the grid (gaps, overlaps, misspelled types, a customer type without an account).
2. Stops if the document has not been saved since it was generated, which means it has not been reviewed yet, unless you confirm you reviewed it.
3. Checks Homerun for entries already on that day, and stops to ask if there are any. It never edits or deletes existing entries.
4. Matches each type, account and opportunity to Homerun, and leaves out any row it cannot match exactly rather than guessing.
5. Shows a preview of every entry it will submit, what it leaves out (lunch, personal time, unmatched rows) and rows still marked proposed, then asks **Submit** or **Cancel**.

Only after you choose Submit does it add the entries, one at a time, stopping at the first failure without retrying.

Needs the Homerun MCP server connected. Without it, the skill stops and nothing is submitted.

**Example prompts:**
- `/submitting-timesheet-to-homerun timesheet-2026-11-17.docx`
- `/submitting-timesheet-to-homerun` (lists the timesheets in the folder and asks which)
