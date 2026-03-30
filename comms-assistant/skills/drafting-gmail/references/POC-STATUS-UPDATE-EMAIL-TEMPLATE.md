# PoC Status Update Email Template

## Purpose

For drafting a follow-up email to prospects or customers after a PoC-related interaction. This is a client-facing email, so the tone should be professional and polished. The skill extracts relevant information from user-provided sales notes and formats it into a concise status update email.

## Input Required

- Sales notes (provided by the user)
- Communication mode: In-Person, Zoom, or Ms Teams (infer from notes if possible, otherwise ask)
- Date of communication (infer from notes if possible, otherwise ask)
- Recipient name(s) for the greeting

## Email Format

The email must follow this exact structure:

```
Subject: {PoC or Company Name} Status Update | {YYYY-MM-DD}

Hi {Recipient first name(s)},

Thank you for {today's session / our call today / our meeting today}. Here is a quick summary of what we covered and the next steps.

{Communication Mode} | {Date}
Attendees: {comma-separated names}

What's Achieved
• {Concise point}
• {Concise point}
• {Concise point}

What's Next
• {Concise point with owner in parentheses}
• {Concise point with owner in parentheses}
• {Concise point with owner in parentheses}

Please let me know if I missed anything or if you have any questions.

Best regards,
Jek Bao Choo
```

## Formatting Rules

- Communication mode must be one of: *In-Person*, *Zoom*, *Ms Teams*
- Each section (Achieved, Next) has a maximum of 3 bullet points. Fewer is fine
- Bullet points must be concise, one sentence each
- Do not use " — " or " - " to connect clauses. Write short, direct sentences instead
- Extract and infer from the sales notes. Do not fabricate information
- If a section has no relevant content from the notes, use a single bullet: "None identified"
- What's Next items should include the owner in parentheses, e.g. "(Datadog)" or "(MOX team)"
- Always include a blank line before "What's Achieved" and before "What's Next"
- The opening line should reference the type of interaction (session, call, meeting) naturally
- Use `•` for bullet points

## Review Checklist

- Subject line includes the PoC/company name and date
- Communication mode and date are correct
- Attendee names are accurate and complete
- Each section has at most 3 bullet points
- Bullet points are concise and factual
- What's Next items have owners
- Tone is professional and client-appropriate
- No sensitive or confidential information included unintentionally
