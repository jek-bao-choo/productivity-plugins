# Datadog Demo Deck — Slide Flow

The template `assets/2026_Datadog_Presentation_Template.pptx` contains ~20 pre-designed,
Datadog-branded slides (purple/violet/white palette, Datadog logo) covering every
presentation need. Build the output deck to this preferred flow.

## Preferred slide flow

| # | Slide | Agenda part | Content source (from meeting notes) |
|---|-------|-------------|-------------------------------------|
| 1 | Title / customer intro | — | Customer name, logo, presenter, date |
| 2 | Agenda | — | Six-part agenda table built with `build_agenda.py` (see [agenda.md](agenda.md)) |
| 3 | Customer's top 3 challenges | Intro & Whiteboard | Pains / problems raised by customer |
| 4 | Datadog's proposed 3 use cases | Intro & Whiteboard | The 3 use cases mapped to the challenges |
| 5 | Current state vs. target state | Intro & Whiteboard | Where they are now vs. desired outcome |
| 6 | Benefits tracker: after Intro | Intro & Whiteboard | `build_agenda.py --benefits intro` |
| 7 | Use Case 1 section divider | Observe | Use case 1 title |
| 8 | Use Case 1 details + demo | Observe | Capabilities, demo talking points for UC1 |
| 9 | Benefits tracker: after Observe | Observe | `build_agenda.py --benefits observe` |
| 10 | Use Case 2 section divider | Act | Use case 2 title |
| 11 | Use Case 2 details + demo | Act | Capabilities, demo talking points for UC2 |
| 12 | Benefits tracker: after Act | Act | `build_agenda.py --benefits act` |
| 13 | Use Case 3 section divider | Secure | Use case 3 title |
| 14 | Use Case 3 details + demo | Secure | Capabilities, demo talking points for UC3 |
| 15 | Benefits tracker: after Secure | Secure | `build_agenda.py --benefits secure` |
| 16 | Recap section divider | Why Datadog | Static |
| 17 | Current state vs. target state recap | Why Datadog | Mirrors slide 5, post-use-case |
| 18 | Capability recap: Datadog vs others | Why Datadog | Datadog vs incumbents / competitors |
| 19 | Takeaways | Why Datadog | Key messages |
| 20 | Business value summary | Why Datadog | Quantified value, ROI, outcomes |
| 21 | Benefits tracker: after Why Datadog | Why Datadog | `build_agenda.py --benefits why_datadog` |
| 22 | Customer success + next steps divider | Next Steps & Close | Static |
| 23 | Relevant customer story + next steps | Next Steps & Close | Reference story + strategic/technical next steps |
| 24 | Benefits tracker: after Next Steps & Close | Next Steps & Close | `build_agenda.py --benefits next_steps`; every row filled in, doubles as the full benefits recap |
| 25 | Thank you / contacts | — | Presenter contacts |
| 26 | Optional reference resources | — | Docs, links (include only if useful) |

## Mapping notes

- **Agenda first.** Slide 2 is always the six-part agenda. Use Case 1 is the Observe
  use case, Use Case 2 is Act, Use Case 3 is Secure, so the use-case slides (7-14) follow
  the agenda order. The agenda's use case titles must match the titles on slides 4, 7, 10
  and 13.
- **Benefits trackers** (6, 9, 12, 15, 21, 24) close each part. Each is a duplicate of
  the agenda slide (`add_slide.py unpacked/ slide2.xml`) rebuilt with
  `build_agenda.py --benefits <part> --slide <new slide file>`. They replace nothing in the
  template; they are added on top of its 20 source slides.

- **Match content type to layout.** Section dividers (7, 10, 13, 16, 22) use the
  template's divider layout. Comparison slides (5, 17, 18) use two-column / vs. layouts.
  Use-case detail slides (8, 11, 14) use content + visual layouts.
- **Analyze the template first** with `thumbnail.py` to see which source slide in the
  template matches each row above, then duplicate that source slide with `add_slide.py`.
- **Preserve Datadog branding** — do not change the palette, logo, or master styling.
  Only replace placeholder text and visuals with customer-specific content.
- **Skip slide 26** (reference resources) if the notes provide no useful links.
- **Section dividers** (7, 10, 13, 16, 22) are duplicated from the template's
  section-divider source slide; only the title text changes.
