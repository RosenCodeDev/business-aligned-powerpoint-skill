# Intent Modes

The intent mode determines what the deck is trying to achieve and how the slide
flow and call to action are shaped. Apply on top of the chosen voice profile
(`60_voice_system.md`). One dominant intent per deck.

## Choosing the intent
If the user states it, use it. Otherwise infer from the request:

| Signal in the request | Intent |
|---|---|
| update, summary, overview, status | Inform |
| recommendation, proposal, business case | Recommend |
| approval, decision, choose, options | Decide |
| alignment, stakeholders, rollout, ways of working | Align |
| vision, keynote, motivate, launch | Inspire |

If still unclear, default to **Inform**.

## 1. Inform
Explain facts, updates, findings, or status without necessarily asking for a
decision. Emphasize clarity, completeness, neutral explanation. Avoid
over-selling and premature recommendations.
- Flow: introduce_topic → explain / show_data / show_trend_with_key_message →
  `summary` ("what to know next"). Neutral; no hard CTA.

## 2. Recommend
Present a preferred course of action and why it is best. Emphasize a clear
recommendation, rationale, benefits, risks/mitigations, alternatives considered.
Do not hide trade-offs or end without a recommendation.
- Flow: lead with the recommendation (`summary`) → rationale (`explain`) →
  options/trade-offs (`compare_two_options`) → risks (`explain`) → recommendation.

## 3. Decide
Enable a specific decision. Emphasize the decision required, options, evaluation
criteria, risks, business impact, and consequences of delay. Avoid long
background and ambiguous asks.
- Flow: state the decision (`summary`/title) → options with criteria
  (`compare_two_options`, `show_data`) → consequences → explicit decision request
  (slide-level `conclusion` + closing `summary`). **Always state the decision required.**

## 4. Align
Create shared understanding and agreement. Emphasize common goals, rationale,
roles and responsibilities, dependencies, next steps. Avoid overly directive or
heavy executive framing.
- Flow: context (`explain`) → roles/dependencies (`show_org_chart`, `show_data`,
  `show_process`) → next steps. **Always state next steps and ownership.**

## 5. Inspire
Motivate around a vision, opportunity, or transformation. Emphasize vision,
possibility, emotional relevance, ambition, momentum. Avoid dense data and dry
status reporting.
- Flow: current reality (`explain`) → contrast what-is/what-could-be
  (`compare_two_options`, `show_trend_with_key_message`) → turning point
  (`section_divider`) → forward-looking close. **End on a motivating message.**

## Calls to action (summary)
- Decide → state the decision required. Align → state next steps and ownership.
- Inspire → end with a motivating, forward-looking message.
- Recommend → always include a clear recommendation unless neutral analysis is
  explicitly requested. Inform → no hard CTA.

## Deck profiles (output character — inferred from the brief)
Infer ONE profile from the user's opening description; it sets the visual mix
and per-slide density defaults (and a default voice profile). State it in the
Phase 2 summary; only ask if the brief gives no signal. The slide count and
audience still apply on top.

| Profile | Signals in the brief | Visual mix | Density | Default style |
|---|---|---|---|---|
| **Editorial report** | "report", "white paper", "long-form", "article" | prose-forward, images on most sections, occasional chart | fuller slides; `paragraphs` not bullets | longform |
| **Financial / performance** | "results", "KPIs", "performance", "budget", "P&L" | chart- and table-heavy; KPI dashboards, waterfalls | dense; numbers carry the slide | consulting |
| **Executive narrative** | "board", "strategy", "recommendation", "decision" | lean; stat callouts, the odd diagram; few images | low per-slide; one idea per slide, action titles | consulting |
| **Visual / marketing** | "vision", "launch", "story", "inspire" | image-heavy; hero statements, big stats, banners | light text; the image/number carries it | consulting |
| **General** (default) | no clear signal | balanced text + a visual per content slide | aim for substance; avoid 3-bullet slides | from the writing-style answer |

Density rule for every profile except where noted: a content slide should carry
a substantive point set OR a visual — if it would be only ~3 short bullets, add
an image/graphic/stat (`stat_callout`, `icon_rows`, a chart) or merge it. The
gate's `density` warning flags thin slides.
