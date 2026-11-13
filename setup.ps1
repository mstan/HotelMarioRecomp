param([string]$Bios = "", [string]$Disc = "", [ValidateRange(1,64)][int]$Jobs = 2)
$ErrorActionPreference = "Stop"
& git -C $PSScriptRoot submodule update --init --recursive
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& (Join-Path $PSScriptRoot "tools/build.ps1") -Bios $Bios -Disc $Disc -Jobs $Jobs
exit $LASTEXITCODE
