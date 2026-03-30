# PoC Status Update Template

## Purpose

For updating the Datadog internal team on Proof of Concept status after a customer or prospect interaction. The skill extracts relevant information from user-provided sales notes and formats it into a concise status update.

## Input Required

- Sales notes (provided by the user — can be raw text, bullet points, or pasted notes)
- Communication mode: In-Person, Zoom, Ms Teams, or Email (infer from notes if possible, otherwise ask)
- Date of communication (infer from notes if possible, otherwise ask)

## Message Format

The draft message must follow this exact structure in Slack mrkdwn:

```
*Attendees*: {Comma-separated names of attendees/recipients, extracted from sales notes}

*{Communication Mode}* | {Date of communication, YYYY-MM-DD}

*What's Achieved*
• {Concise bullet point — max 1 sentence}
• {Concise bullet point — max 1 sentence}
• {Concise bullet point — max 1 sentence}

*What's Blocking*
• {Concise bullet point — max 1 sentence}
• {Concise bullet point — max 1 sentence}
• {Concise bullet point — max 1 sentence}

*What's Next*
• {Concise bullet point — max 1 sentence}
• {Concise bullet point — max 1 sentence}
• {Concise bullet point — max 1 sentence}
```

## Formatting Rules

- Communication mode must be one of: *In-Person*, *Zoom*, *Ms Teams*, *Email*
- Each section (Achieved, Blocking, Next) has a **maximum of 3** bullet points — fewer is fine if the notes don't warrant 3
- Bullet points must be concise, one sentence each, no filler
- Do not use " — " or " - " to connect clauses within bullet points. These patterns make the message sound AI-generated. Write short, direct sentences instead. For example, write "MOX uses a threat-based security approach" not "MOX's security approach is threat-based — aligns well with Datadog positioning"
- Extract and infer from the sales notes; do not fabricate information
- If a section has no relevant content from the notes, use a single bullet: "None identified"
- Always include a blank line before each section heading (`*What's Achieved*`, `*What's Blocking*`, `*What's Next*`)
- Use Slack mrkdwn formatting: `*bold*` for headers, `•` for bullet points

## Review Checklist

- Communication mode and date are correct
- Attendee names are accurate and complete
- Each section has at most 3 bullet points
- Bullet points are concise and factual (derived from sales notes)
- No sensitive or confidential information included unintentionally
