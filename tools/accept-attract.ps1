param(
    [Parameter(Mandatory = $true)][string]$Bios,
    [Parameter(Mandatory = $true)][string]$Disc,
    [string]$Runtime = ""
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$engine = Join-Path (Split-Path -Parent $root) "cdirecomp"
if (-not $Runtime) {
    $Runtime = Join-Path $root "build/HotelMarioRecomp.exe"
}
$probe = Join-Path $engine "tools/hotelmario_launch_probe.py"

if (-not (Test-Path -LiteralPath $Runtime)) {
    throw "HotelMarioRecomp is not built at $Runtime. Run tools/build.ps1 first."
}
if (-not (Test-Path -LiteralPath $probe)) {
    throw "The pinned cdirecomp checkout is missing $probe."
}

py -3 $probe $Runtime $Bios $Disc `
    --seconds 55 --timeout 180 `
    --quick --compact --accept-attract
exit $LASTEXITCODE
