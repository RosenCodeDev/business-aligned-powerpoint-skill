# Runtime Bootstrap — making the OW runtime available

Decks are built ONLY by running the template-native runtime
(`deck_system_runtime_clean.zip`, which bundles `ow_default.pptx`). That file must
be present in the Code Interpreter sandbox. **Run the preflight in Phase 3 —
right after the brief is confirmed, before deep work — so a missing runtime is
caught early, not after the user has approved an outline.**

## Why this sometimes fails (and how the gate fixes it)
Two platform facts drive every failure mode:
1. The operative locate/extract steps cannot live only in this doc — Knowledge is
   surfaced by retrieval, not guaranteed in context. So the snippet is also
   inlined in the Instructions field (always in context).
2. A GPT's Knowledge files are copied into `/mnt/data` **lazily, on the first
   Code Interpreter run** — and only if Code Interpreter is enabled. So you must
   *actually execute* the preflight (not narrate it); the act of running it is
   what stages the files. A first miss is retried after a short wait before
   concluding anything is missing.

The preflight ends by **printing a version line** that is a hard gate: do not
build, and never emit a `.pptx`, until you have seen `RUNTIME OK v…` printed in
THIS chat. Conclude the runtime is missing ONLY if the executed snippet prints
`RUNTIME MISSING` (it also lists `/mnt/data` so you can see what is actually
there).

**Setup check (GPT builder):** Code Interpreter / Data Analysis must be ENABLED
on the GPT, and `deck_system_runtime_clean.zip` uploaded as Knowledge under that
exact name. If CI is off, Knowledge files never reach a sandbox and the only path
is attaching the zip to each chat.

## Preflight (early, once per chat)
Run the **runtime-gate snippet from the Instructions field (Rule 3)** — that is
the canonical copy. Equivalently, once anything is extracted you can run
`python <src>/bootstrap.py` (shipped inside the runtime zip). Both do the same
thing: search `/mnt/data`→`/mnt`→cwd, extract once to `/mnt/data/ow_runtime`,
retry the lazy knowledge-file copy, then print `RUNTIME OK v…` or `RUNTIME
MISSING` (with a `/mnt/data` listing). **Execute it — do not narrate it.**

## Rules
1. **Search small dirs first** (`/mnt/data`, then `/mnt`, then cwd). Never scan all
   of `/` — it is slow and its output gets truncated.
2. **Extract once** to `/mnt/data/ow_runtime` and reuse it for the whole chat.
3. **Gate on the print.** If you did not see `RUNTIME OK v…`, you have not loaded
   the runtime — fix that before doing anything else.
4. **If MISSING: STOP and ask the user to attach `deck_system_runtime_clean.zip`
   to the chat now** (dragging it into the message box places it in `/mnt/data`).
   Explain it is a one-time step for this chat. NEVER fall back to a built-in
   slides tool, pptxgenjs, or hand-built python-pptx.

## Building (Phase 6) — re-verify first
Sandboxes idle-reset, so re-run the preflight at build time too. Only build once
`RUNTIME OK v…` has printed. Then:
```
python src/generate_deck.py --template ow_default.pptx --deck <json> --output <pptx>
```
`ow_default.pptx` is bundled in the zip. The build prints a summary (version,
slides, ignored unknown keys) — read it and patch the JSON on any error.

## Persistence
Keep `research.json` and the extracted runtime in `/mnt/data`. If the sandbox
idle-resets mid-chat, re-run the preflight; at most a re-attach of the zip is
needed — never a redo of the source analysis.

## Image modes — placeholder vs generate-and-embed

**When the brief asks for imagery/photography, you must actually use image slots.**
Real photography comes only from an image slot — the cover (`introduce_topic.image`),
a person photo (`introduce_person.photo`), or a `compose` `image` block. Do NOT
substitute the runtime's decorative vector graphics (drawn cars, simple shapes,
icon motifs) as a stand-in for requested photography — a drawn vector is an
illustration, not the photo the brief asked for. Every image slot MUST carry a
concrete subject description (the thing to photograph, e.g. "a modern electric
SUV charging at a city kerb at dusk"); never create an image slot with an empty
description — an empty prompt yields a generic or abstract result. The runtime
wraps the description in the photoreal prompt (`build_image_prompt`); your job is
to supply a specific subject.
The image mode sets how every image slot is filled. **Placeholders is the
default and is used unless the user has EXPLICITLY chosen to generate and embed
real images** — either by picking **"Generate & embed real photos"** from the
Phase-1 image menu, or by clearly asking for it in words ("generate and embed the
photos", "I want real images in the file"). Picking that menu option counts as the
explicit request — honour it. What does NOT trigger embed: a brief that merely
*mentions* "imagery" or "AI-generated images" in passing without choosing embed —
that stays placeholders.

- **Placeholders** (default, safest): each slot renders a swappable box showing a
  ready-to-paste, photorealistic ChatGPT prompt. Nothing is generated; the human
  fills it later. This is the correct choice whenever you are not explicitly asked
  to embed, OR you cannot produce a genuine photograph (see the hard rule below).
- **Generate & embed** (only on explicit request): BEFORE building, for each image
  slot generate the picture with your image tool. **Build the prompt the same way
  the runtime does for placeholders — `build_image_prompt(description, aspect)` in
  `images.py`, i.e. "A photograph of {description}. Photorealistic, real
  photography, natural lighting, sharp focus, no CGI, no illustration, no text or
  logos. Aspect ratio {aspect}."** Do NOT send the bare slot description — without
  this anchor the image tool drifts to illustration/CGI. Then **save the file into
  `/mnt/data`** (e.g. `/mnt/data/img_<name>.png`), set
  `images: {"<name>": {"path": "/mnt/data/img_<name>.png"}}` in the deck JSON, and
  point the slide's `image.source` (or a compose image block's `source`) at
  `<name>`. The runtime embeds the real picture.
- **None**: omit image slots entirely (text/graphics only).

**HARD RULE — never fake a photograph.** A real photo comes ONLY from your image
tool (in embed mode). You must NEVER fabricate an image in code — no PIL,
matplotlib, drawing, gradients, silhouettes, or shape collages — and pass it off
as a photo via `path`. A code-drawn panel is an illustration, not a photograph,
and embedding one to satisfy a photo request is a defect. The runtime's
`allow_image_generation` flag is only an offline brand-gradient stand-in; it is
**never** a way to satisfy a photo request — leave it `false`. If you are in
embed mode but cannot produce a genuine photograph (no usable image tool, or you
cannot save into `/mnt/data`), **fall back to placeholders and tell the user
plainly** that no images were embedded. Drawing your own is not an option.
Non-photographic visuals (diagrams, charts, maps, backgrounds) come from the
runtime's own graphics — but those are never substituted for a requested photo.

Notes: real embedded pictures are named `IMAGE:<name>`; only *unfilled*
placeholders are `REPLACE:<name>` (the gate counts those as work-to-do).
