# Datadog Demo Deck — Slide Flow

The template `assets/2026_Datadog_Presentation_Template.pptx` contains ~20 pre-designed,
Datadog-branded slides (purple/violet/white palette, Datadog logo) covering every
presentation need. Build the output deck to this preferred flow.

## Preferred slide flow

| # | Slide | Content source (from meeting notes) |
|---|-------|-------------------------------------|
| 1 | Title / customer intro | Customer name, logo, presenter, date |
| 2 | Agenda | Derived from this flow |
| 3 | Customer's top 3 challenges | Pains / problems raised by customer |
| 4 | Datadog's proposed 3 use cases | The 3 use cases mapped to the challenges |
| 5 | Current state vs. target state | Where they are now vs. desired outcome |
| 6 | Use Case 1 section divider | Use case 1 title |
| 7 | Use Case 1 details + demo | Capabilities, demo talking points for UC1 |
| 8 | Use Case 2 section divider | Use case 2 title |
| 9 | Use Case 2 details + demo | Capabilities, demo talking points for UC2 |
| 10 | Use Case 3 section divider | Use case 3 title |
| 11 | Use Case 3 details + demo | Capabilities, demo talking points for UC3 |
| 12 | Recap section divider | Static |
| 13 | Current state vs. target state recap | Mirrors slide 5, post-use-case |
| 14 | Capability recap: Datadog vs others | Datadog vs incumbents / competitors |
| 15 | Takeaways | Key messages |
| 16 | Business value summary | Quantified value, ROI, outcomes |
| 17 | Customer success + next steps divider | Static |
| 18 | Relevant customer story + next steps | Reference story + strategic/technical next steps |
| 19 | Thank you / contacts | Presenter contacts |
| 20 | Optional reference resources | Docs, links (include only if useful) |

## Mapping notes

- **Match content type to layout.** Section dividers (6, 8, 10, 12, 17) use the
  template's divider layout. Comparison slides (5, 13, 14) use two-column / vs. layouts.
  Use-case detail slides (7, 9, 11) use content + visual layouts.
- **Analyze the template first** with `thumbnail.py` to see which source slide in the
  template matches each row above, then duplicate that source slide with `add_slide.py`.
- **Preserve Datadog branding** — do not change the palette, logo, or master styling.
  Only replace placeholder text and visuals with customer-specific content.
- **Skip slide 20** (reference resources) if the notes provide no useful links.
- **Section dividers** (6, 8, 10, 12, 17) are duplicated from the template's
  section-divider source slide; only the title text changes.
