param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$SkillRoot = Join-Path $RepoRoot "distributions\ai-platform\deck-builder"
$DistRoot = Join-Path $RepoRoot "dist"
$Archive = Join-Path $DistRoot "deck-builder.zip"

& $Python (Join-Path $PSScriptRoot "validate_package.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& $Python -m unittest discover -s (Join-Path $RepoRoot "tests") -v
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

New-Item -ItemType Directory -Force -Path $DistRoot | Out-Null
& $Python (Join-Path $PSScriptRoot "package_skill.py") $Archive
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
