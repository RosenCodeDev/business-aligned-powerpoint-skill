# Runtime verification

## Verified package identity

The exact runtime archive available in the prior migration package is:

- Filename: `deck_system_runtime_clean.zip`
- Size: 1,267,729 bytes
- SHA-256: `c595e17c097d16aa33880193fceec3928e7a08cfcca603ffa82f0a03a2f7663d`
- Runtime `__version__`: **2.6.18**
- Internal template: `ow_default.pptx`
- Internal file count: 539 files (500 SVG icons, 31 Python files, 3 XML files, 2 JSON files, 1 XLSX, 1 PPTX, 1 TXT)

The copy in the previous migration ZIP is byte-for-byte identical to the currently available original runtime archive.

## Execution environment actually verified

The bundled automated suite was executed on:

- OS: Linux 6.18.44, x86_64, glibc 2.41
- Python: 3.13.5 (GCC 14.2.0)
- Python executable: `/opt/pyvenv/bin/python`
- Writable workspace used: `/mnt/data`
- Test result: 174 passed, 1 skipped, 0 failed

See `TEST_RESULTS.txt` for the exact command and output.

## Python version requirement

The runtime archive does **not** declare a minimum or maximum Python version. Therefore an exact supported Python-version range is unavailable.

What is verified:

- Python 3.13.5 works in the present Linux environment.
- The source uses ordinary Python 3 syntax and packages listed in `requirements.txt`.
- A local deployment should pin and test a Python version rather than assuming all Python 3 versions are supported.

## Dependency requirements

The archive's exact `requirements.txt` is:

```text
python-pptx>=0.6.23
lxml>=5.0.0
Pillow>=10.0.0
pytest>=8.0.0
openpyxl>=3.1
svgelements>=1.9
fonttools>=4.40
pyyaml
```

Installed versions used in this verification environment:

| Dependency | Observed version | Notes |
|---|---:|---|
| python-pptx | 1.0.2 | Exceeds declared minimum |
| lxml | 6.1.1 | Exceeds declared minimum |
| Pillow | 12.3.0 | Exceeds declared minimum |
| pytest | 9.0.2 | Test-only/runtime verification |
| openpyxl | 3.1.5 | Exceeds declared minimum |
| fonttools | 4.63.0 | Exceeds declared minimum |
| PyYAML | 6.0.3 | No minimum declared |
| svgelements | vendored VERSION 1.9.6 | No installed distribution was detected; the runtime includes `src/svgelements/` |

For reproducible local use, create a lock file from a known-good environment rather than relying indefinitely on lower-bound-only requirements.

## Fonts and text metrics

The template theme references:

- Marsh Serif as the major/primary typeface.
- Noto Sans as the minor/body typeface.

The template contains six `ppt/fonts/*.fntdata` embedded font parts. The runtime's `textmetrics.py` explicitly warns that embedded PowerPoint faces can be obfuscated or not loadable by `fontTools`.

Its text-metric resolution order is:

1. Loadable embedded template face.
2. A system proxy:
   - body/minor: DejaVu Sans, Liberation Sans, or Arial.
   - major: DejaVu Serif, Liberation Serif, or Times.
3. A flat character heuristic if no font file can be found.

On Unix-like systems, the code searches only:

- `/usr/share/fonts`
- `/usr/local/share/fonts`
- `~/.fonts`

**Visual parity therefore benefits from having Marsh Serif and Noto Sans legally available to PowerPoint/the rendering environment, but the build can still run without them.** Missing brand fonts can change line breaks and visual appearance even if the gate passes with proxy metrics.

## External binaries

No runtime Python source in the supplied archive invokes LibreOffice, `soffice`, Inkscape, ImageMagick, or `fc-match` through subprocess calls.

Therefore:

- PowerPoint generation itself does not require those external binaries.
- The bundled test suite does not require Microsoft PowerPoint.
- PowerPoint is still the authoritative viewer for certain Office-native objects, especially native ChartEx treemaps.

The current host happens to have LibreOffice, Fontconfig, ImageMagick, and Inkscape installed, but their presence is not a verified runtime requirement.

## Environment variables

No mandatory environment variable is declared.

One optional source-level switch exists:

- `OW_MEASURED_WRAP`: toggles measured wrapping behavior in `compiler.py` when present.

The variable `OAI_IS_JUPYTER_KERNEL=0` used in `TEST_RESULTS.txt` is **host-specific test hygiene**, not a runtime setting. It only disabled an unrelated spreadsheet warm-up hook injected by this execution environment.

## Filesystem assumptions

The ChatGPT bootstrap is environment-specific:

- extraction destination: `/mnt/data/ow_runtime`
- search roots: `/mnt/data`, `/mnt`, then current working directory
- expected archive pattern: `*runtime*clean*.zip` or `*runtime*.zip`
- lazy GPT Knowledge staging is assumed to place files into `/mnt/data`

The actual generator can be used without this bootstrap if a local agent already knows the extracted runtime path. `generate_deck.py` accepts explicit template, deck-spec, and output paths.

## Network requirements

The runtime build and bundled tests do not require network access.

Network access is only needed for higher-level agent workflows when:

- researching current facts on the web,
- retrieving external source material,
- or generating images through an external/provider image model.

A source-only or placeholder-image deck can be built offline.

## Local Windows portability

The core OOXML/Python runtime is plausibly portable, but the supplied ChatGPT bootstrap is **not Windows-native as written**. Known adaptations:

1. Replace `/mnt/data` and `/mnt` bootstrap roots with a configurable workspace directory.
2. Add `%WINDIR%\Fonts` (and any corporate font directory) to `textmetrics.py` font search paths if embedded faces are not loadable.
3. Use `sys.executable` or a configured Python command in local test/process wrappers; some bundled tests call `python` literally.
4. Pass absolute paths to the template and deck specification to avoid working-directory assumptions.
5. Test native ChartEx treemaps in desktop Microsoft PowerPoint; headless renderers may show them blank even when the PPTX is valid.
6. Ensure the user or organization has lawful access to the required branded template/fonts/assets; technical portability does not establish reuse rights.

## Codex / local Agent Skill portability

A local Codex skill should:

- treat the runtime directory as a skill-relative dependency rather than relying on GPT Knowledge staging,
- expose a configurable workspace path instead of hard-coding `/mnt/data`,
- invoke `src/generate_deck.py` with absolute paths,
- preserve the non-overridable `gate_result.json` check,
- provide web/image tools only when configured, otherwise use uploaded evidence and image placeholders,
- and run a local rendering/inspection step appropriate to the environment if visual QA beyond structural gate checks is required.

## Version-string caution

`runtime.py` is authoritative for the runtime version and reports `2.6.18`. Some prose/examples elsewhere in the archive or knowledge base contain older example/version labels; they should not override the imported `runtime.__version__`.
