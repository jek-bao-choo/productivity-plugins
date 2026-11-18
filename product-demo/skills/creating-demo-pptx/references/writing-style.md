# Writing Style: Concise, Succinct, Short

Every word on a slide competes with the presenter. The audience should take in a slide in
a few seconds and then listen. Write the least text that still makes the point, and let the
demo and the presenter carry the rest.

## Rules

1. **Rule of 3.** Three bullets per text box, four at most. Three takeaways. Three
   next steps per column.
2. **Fragments, not sentences.** "MTTR down 40%", not "We expect to reduce MTTR by 40%."
   No full stops at the end of bullets.
3. **One idea per line.** If a line needs "and" to join two ideas, split it or drop one.
4. **Lead with the outcome or the number.** "Payments fixed before customers call", not
   "Datadog can help your team to fix payments faster so that customers do not call".
5. **Customer's words over Datadog's.** Use the customer's terms (bill payments, call
   center, fraud agent) instead of generic product language.
6. **Digits for numbers.** "6 success criteria", "40%", "2 weeks".
7. **Cut filler.** Drop: *in order to, leverage, utilize, seamless(ly), robust,
   comprehensive, holistic, cutting-edge, best-in-class, world-class, state-of-the-art,
   empower, unlock, game-changing, very, really, basically, actually*.
8. **No dash joiners.** Do not join clauses with " — " or " - ". Use a comma, a colon or
   a new line. (The agenda's "—" empty-cell marker is fine.)
9. **Cut, don't shrink.** If text does not fit, remove the weakest point. Never reduce the
   font below the template's sizes to fit more words, and never pad an empty area with
   extra bullets. White space is fine.

## Word limits

| Element | Limit |
|---|---|
| Slide title | 8 words |
| Section divider subtitle (use case name) | 8 words |
| Heading inside a card or column | 6 words |
| Bullet or body line | 12 words |
| Challenge or pain point description | 15 words |
| Takeaway | 10 words |
| Business value line | 10 words, number first |
| Next step | 8 words |
| Whole content slide (excluding title) | 60 words |
| Agenda use case title | 8 words |
| Agenda quote (verbatim) | 20 words; trim with "…" keeping the customer's exact words |
| Agenda question | 15 words |
| Agenda note (From My Notes) | 12 words |
| Agenda attribution | 4 words, role not name |
| Benefit line (trackers) | 8 words |
| What Demonstrates It | 5 entries, 4 words each |

`build_agenda.py` enforces the agenda and tracker limits and stops with a list of lines to
shorten. `check_wording.py` checks the rest of the deck (see below).

## Before and after

| Before | After |
|---|---|
| Our solution provides comprehensive end-to-end visibility across your entire stack | One view across every service |
| Reduce Mean Time To Resolution by approximately 40% through faster root cause analysis | MTTR down 40% |
| Engineers currently spend a large amount of time switching between different tools | Less tool switching for engineers |
| Leverage Datadog's robust log management capabilities to lower costs | Lower log costs, same search power |
| Datadog Cluster Agent — collects cluster-level metadata and reduces API server load | Cluster Agent: less load on the API server |

## Check the finished deck

Run after packing, as part of the Step 5 visual check loop:

```bash
python3 $SCRIPTS/check_wording.py output.pptx
```

It lists every slide with a line over 12 words, a title over 8 words, more than 60 words
in total, filler words, or dash joiners. Agenda and tracker slides are skipped (the agenda
script already checked them). Shorten what it reports, rebuild, and run it again until it
reports nothing. Static template text you did not write (for example the "Relatable
Customer Success & Next Steps for <Customer>" divider) can be left as is.
