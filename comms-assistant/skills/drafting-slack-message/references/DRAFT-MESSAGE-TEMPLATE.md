# Draft Message Review

## Target
- **Channel**: {#channel-name} ({channel-id})
- **Type**: {New message | Thread reply}
- **Thread parent**: {parent message summary, if thread reply}

## Context Read
{Brief summary of the channel/thread context that informed the draft}

## Draft Content

---
{The actual message content in Slack mrkdwn format}
---

## Checklist Before Saving
- [ ] Tone is appropriate for the channel audience
- [ ] Key points are covered
- [ ] No sensitive or confidential information included unintentionally
- [ ] Mentions (@user) are correct
- [ ] Links are valid

## Action
Once confirmed, the draft will be saved to Slack using `slack_send_message_draft`.
The user can then review and send it from **Drafts & Sent** in Slack.
