# Brand Guidelines (Oliver Wyman)

The runtime renders into `ow_default.pptx`, which already carries the brand —
fonts, colour palette, logos, footers, spacing, table and chart styles. Do not
override them; author content that fits them.

**All quantitative design facts — font sizes, spacing, the grid, outlines, bullet
styles, colours, and the auto-fit floor — live in `50_design_system.md`, generated
from the engine and the single source of truth. The engine enforces them; the GPT
does not set them. This file holds only the authoring judgment the GPT controls.**

## Authoring notes (what the GPT controls)
- Title case for slide titles; sentence case for body text.
- Provide bullet content as plain text items — never type a "•" or "-" glyph into
  the text; the runtime applies the real OW bullet styles (glyphs, indents) for you.
- Charts: keep legends and labels minimal and let the title carry the message.
- Cover, Section, and legal slides stay clean — do not add a conclusion or footnote.
- Put source/disclaimer text in `footnote`; keep the template's footer and numbering.
- Build only through the runtime intents — never hand-place shapes or geometry.

## Tone of voice
See `60_voice_system.md` — the OW house voice applies to every deck and sits
above the chosen voice profile.
