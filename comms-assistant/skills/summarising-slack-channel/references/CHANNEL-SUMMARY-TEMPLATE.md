# Channel Summary: #{channel-name}

**Period**: {start-date} to {end-date}
**Messages reviewed**: {total-count}
**Filtered out (noise)**: {noise-count} (bot messages, bumps, system notifications)
**Q&A blocks generated**: {qa-count}

## Summary Overview

{2-3 sentence overview of the channel activity during this period. Mention the most common themes and any critical/urgent items.}

**Top themes**: {theme1}, {theme2}, {theme3}, {theme4}, {theme5}

---

<!-- For 15 or fewer Q&A blocks, list them sequentially. For more than 15, group under theme headings as shown below. -->

## Theme: {Theme Name}

---

Date: {YYYY-MM-DD — the date the Slack message was posted}

Question: {The question that the Slack message is discussing in a sentence.}

Answer: {A paragraph summarizing the discussion or resolution, informed by thread replies where available. If a specific technical solution, command, or key point is mentioned, quote it directly from the text using "double quotes" with the Slack username. For example: According to @jane, "you need to set DD_APM_ENABLED=true in the agent configuration" to resolve the traces not appearing in APM. If the discussion did not reach a conclusion after checking thread replies, state: "The discussion is ongoing/unresolved."}

URLs: {url1 | url2 | url3} or "None" if no URLs exist.

Slack URL: https://dd.slack.com/archives/{channel_id}/p{message_ts_without_dot}

---

Date: {YYYY-MM-DD}

Question: {Next question within the same theme.}

Answer: {Summary paragraph with quoted specifics and attribution.}

URLs: {url1} or "None"

Slack URL: https://dd.slack.com/archives/{channel_id}/p{message_ts_without_dot}

---

## Theme: {Next Theme Name}

---

Date: {YYYY-MM-DD}

Question: {Question in this theme group.}

Answer: {Summary paragraph.}

URLs: {url1} or "None"

Slack URL: https://dd.slack.com/archives/{channel_id}/p{message_ts_without_dot}

---

<!-- Repeat for each theme and Q&A block. -->
