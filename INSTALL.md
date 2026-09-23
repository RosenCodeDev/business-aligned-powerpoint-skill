# Installation

## Codex or another file-capable agent

Copy the installable distribution into the host's skills directory:

```powershell
Copy-Item -Recurse -Force `
  ".\distributions\ai-platform\deck-builder" `
  "$env:USERPROFILE\.codex\skills\deck-builder"
```

Restart or reload the host if it does not detect newly installed skills automatically. Invoke the skill as `$deck-builder`, or ask for an Oliver Wyman-style PowerPoint deck.

## Runtime dependencies

Install the dependencies listed in the distribution:

```powershell
python -m pip install -r ".\distributions\ai-platform\deck-builder\requirements.txt"
```

The skill's wrapper uses the active Python interpreter, verifies the runtime archive hash, and extracts the runtime into a task workspace. It never modifies the canonical skill files.

## Optional fonts

For the closest visual match, use lawfully installed Marsh Serif and Noto Sans fonts. The deck can build without them, but PowerPoint may substitute fonts and reflow text.

