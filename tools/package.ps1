param(
    [Parameter(Mandatory=$true)][string]$Version,
    [string]$Build = "build",
    [string]$Output = ""
)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$engine = [IO.Path]::GetFullPath((Join-Path $root "../cdirecomp"))
$buildDirectory = [IO.Path]::GetFullPath((Join-Path $root $Build))
$arguments = @("-3", (Join-Path $engine "tools/package_runtime_release.py"),
    "--product", "hotelmario", "--version", $Version,
    "--runtime", (Join-Path $buildDirectory "HotelMarioRecomp.exe"),
    "--sdl", (Join-Path $buildDirectory "SDL2.dll"),
    "--config", (Join-Path $engine "player.cfg.example"),
    "--readme", (Join-Path $root "RUNTIME-README.md"),
    "--notices", (Join-Path $engine "THIRD-PARTY-NOTICES.md"))
if (-not $Output) { $Output = Join-Path $root "dist/HotelMarioRecomp-$Version-windows-x64.zip" }
$arguments += @("--out", $Output)
& py @arguments
if ($LASTEXITCODE -ne 0) { throw "Runtime archive audit failed" }
