# OW Voice System — writing-style reference

One deliverable, one voice. The profile is chosen by **audience** and declared in
the brief (`voice_style: consulting | longform`). It sets the *surface* — register,
titles, bullets-vs-prose, sentence mechanics. The *argument structure* (pyramid,
MECE, SCQA opening, headline ladder) is owned by `15_storyline_logic.md` and is
not repeated here. The **house voice** below applies to both profiles and does
not change.

This file is generated from `voice_profiles.py` (+ `voice_prose.py`); edit those,
not this doc. Lint a draft with `generate_deck.py --lint-text`.

## House voice (applies to both profiles)
Precise, senior, understated. Sound like a trusted advisor who has done the work
and formed a view — confident through clarity, not adjectives. Let evidence and
structure persuade; state conclusions plainly and show judgement rather than
enthusiasm.

- **Take a position.** If the analysis supports a conclusion, state it. A bland,
  balanced, view-from-nowhere is the main failure mode to avoid.
- **Concrete verbs that say what happens:** decide, reduce, clarify, prioritise,
  fund, stop, scale, pilot, approve, defer, redesign. Avoid vague-active verbs
  (leverage, enable, enhance, transform, optimise, empower, facilitate) and
  generic claims ("drive value", "best-in-class", "game-changing") unless backed
  by specific evidence.
- **Interpret numbers; never just display them.** Say what a figure means for the
  business question.
- **Handle uncertainty honestly.** Distinguish fact, interpretation, and
  assumption. Don't overclaim ("clearly", "without question") or bury the view
  under hedging — calibrate ("far from certain") rather than hedge everything.
- **Mechanics:** sentence case for body; consistent terminology, capitalisation,
  and number formats; spell out acronyms on first use for mixed audiences; cut
  anything that doesn't change what the reader understands, decides, or asks next.

## Shared foundation (structure lives in 15_storyline_logic.md)
Both profiles render the *same* argument; they differ only in wording. Before
either applies, the storyline is already built per `15_storyline_logic.md`: one
governing message on top, a small MECE set of supporting arguments beneath, the
evidence under each, and an opening pattern (pyramid or SCQA) chosen by Intent
Mode. Read the takeaway titles top-to-bottom and the argument must hold.

The voice profile does not re-decide structure. It decides whether that structure
surfaces as action titles + bullets (consulting) or as topic-sentence-led
paragraphs (longform).

## Choosing the profile
One profile per deck, picked by how the audience will *consume* it:

- **`consulting`** when the deliverable is presented live or skimmed under time
  pressure by a decision forum (board, steering committee, executives) and the
  goal is a fast decision. The artefact is a deck.
- **`longform`** when the deliverable is read off-platform — thought leadership,
  a white paper, a policy or regulatory document, an internal briefing, a board
  pre-read — and the goal is to persuade through a developed argument. The
  artefact reads as a document.

Tie-breaker: *will they read it alone or watch me present it?* Read → longform;
present → consulting. The choice is declared in the brief as
`voice_style: consulting | longform`; the agent echoes the choice and a one-line
reason before generating, and infers-then-confirms it when the brief is silent.

## Profiles
### Profile: `consulting` — action-first
Answer-first slides built from action titles and short, parallel bullets — one idea per slide, the title carries the 'so what'.

**Audiences:** executives, board, steering committee, decision forum, project team
**Select when:** the deliverable is PRESENTED live or skimmed under time pressure, the audience is a decision forum, and the goal is a fast decision. Format: slides.

The discipline is one idea per slide, proven by the title. Everything on the slide exists to support the title's claim; if an element doesn't, cut it (the 'so what?' test). Bullets carry judgement — each is a complete analytical thought ("Speed is constrained by late clarification loops, not capacity"), never a label ("Process speed"). Name the decision plainly ("Decide whether to standardise intake before adding capacity"), and interpret every figure rather than displaying it.

**Titles**

| Rule | Value |
| --- | --- |
| `style` | action-title |
| `max_words` | 15 |
| `voice` | active |
| `must_state_so_what` | yes |

**Body**

| Rule | Value |
| --- | --- |
| `mode` | bullets |
| `bullets_max_per_unit` | 30 |
| `bullets_are` | short parallel fragments, each a complete analytical thought, never a label |
| `bullets_overflow` | engine continues onto the next slide automatically |
| `paragraphs` | discouraged (a short lead-in line is fine) |
| `lead` | answer-first (BLUF) |
| `source_every_number` | yes |

**Sentences**

| Rule | Value |
| --- | --- |
| `register` | telegraphic but not cryptic; strong verbs, concrete nouns |
| `length_variation` | required |
| `hedge_budget_per_unit` | 1 |
| `point_of_view` | required |

**Before → after**

- *Generic:* Customer Churn Analysis
- *Consulting:* Churn rose to 14% in H1, driven entirely by SMB — fixing onboarding recovers ~$8M ARR

- *Generic:* We looked at the data and found several issues with onboarding that may be contributing to customers leaving.
- *Consulting:* Three parallel bullets — "Onboarding takes 3× longer than competitors (18 vs 6 days)"; "60% of churned SMB accounts never completed setup"; "Fixing setup recovers ~$8M ARR by FY27".

### Profile: `longform` — editorial-prose
Flowing, topic-sentence-led paragraphs that develop the argument across sentences, with very limited bullets — like a printed strategy report.

**Audiences:** internal, readers, policy, regulator, thought-leadership, board (pre-read)
**Select when:** the deliverable is READ off-platform (white paper, thought leadership, policy/regulatory doc, board memo), and the goal is to persuade through a developed argument. Format: a document or text-heavy leave-behind.

The discipline is the paragraph, not the bullet. Each paragraph opens with its point and then earns it; sentences run old-to-new so the reader is carried forward; characters are subjects and their actions are verbs ("we decided", not "a decision was taken"). Titles may be evocative — a metaphor or claim with a plain subtitle, in the OW house manner — but the opening paragraph still states the answer. Reserve bullets for genuine enumeration; if a slide is drafting as fragments, it isn't yet longform.

**Titles**

| Rule | Value |
| --- | --- |
| `style` | evocative-or-declarative |
| `max_words` | 14 |
| `voice` | active |
| `must_state_so_what` | no |

**Body**

| Rule | Value |
| --- | --- |
| `mode` | prose |
| `paragraph_topic_sentence` | yes |
| `cohesion` | old-to-new (open with familiar, end with new/emphatic) |
| `nominalizations` | discouraged (characters as subjects, actions as verbs) |
| `bullets` | minimal — only for genuine enumeration |
| `paragraph_words` | ≈40–90; vary length; never 4 same-length in a row |
| `lead` | answer-first opening paragraph |

**Sentences**

| Rule | Value |
| --- | --- |
| `register` | active voice, strong verbs; cut clutter (Paramedic Method) |
| `length_variation` | required |
| `hedge_budget_per_paragraph` | 1 |
| `point_of_view` | required |

**Before → after**

- *Generic:* There are a number of factors that could potentially be considered as contributing to the increase in churn observed during the period in question.
- *Longform:* Churn climbed to 14% in the first half — and almost all of it came from one place. Small-business customers, not enterprise accounts, drove the rise. The cause is mundane but expensive: onboarding takes three times longer than at competitors, and three in five churned SMB accounts never finished setting up. Fix the setup flow and roughly $8 million in recurring revenue comes back.

## Avoiding bland / templated prose
These apply to both profiles and are the highest-leverage quality rules:

- **State a view.** The single biggest lift. If the evidence points somewhere,
  say so.
- **Ban the AI-filler fingerprint.** No "furthermore / moreover / it's worth
  noting / in conclusion"; no "delve / unleash / pivotal / realm / tapestry /
  leverage"; no reflexive rule-of-three for rhythm.
- **Concrete over abstract.** Specific numbers, named mechanisms, vivid anchors —
  not "significant value" or "a number of factors".
- **Vary cadence.** Mix sentence lengths and openings; cap a fast passage with a
  short line; use parallelism deliberately, not by default.
- **Kill hedging stacks.** "may / might / could potentially" → one calibrated
  modal or a flat claim.
- **Read-aloud test.** If you wouldn't say it to a colleague, rewrite it.

## Linting & review
A draft is checked by `generate_deck.py --lint-text <file> --profile <name>`:
deterministic rules flag banned filler, clutter words, over-budget hedging,
over-long titles (consulting), and bullets-where-prose-belongs (longform). The
judgement calls — does the title state a so-what, does each paragraph open with
its point, is there a point of view — are scored by the reviewer rubric (see
`voice_lint.REVIEWERS`). Run generate → lint → revise until the lint passes.
