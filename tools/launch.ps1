param([string]$Bios = "", [string]$Disc = "", [string]$Runtime = "", [switch]$NoLauncher)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
foreach ($name in @("bios", "disc")) {
    $variable = Get-Variable -Name $name
    $sidecar = Join-Path $root ($name + ".cfg")
    if (-not $variable.Value -and (Test-Path -LiteralPath $sidecar)) {
        Set-Variable -Name $name -Value ([IO.File]::ReadAllText($sidecar).Trim())
    }
}
if (-not $Runtime) { $Runtime = Join-Path $root "build/HotelMarioRecomp.exe" }
if (-not (Test-Path -LiteralPath $Runtime)) { throw "Build the player first: tools/build.ps1 -Bios <rom> -Disc <cue>" }
$arguments = @()
if ($Bios) { $arguments += (Get-Item -LiteralPath $Bios).FullName }
if ($Disc) { $arguments += @("--disc", (Get-Item -LiteralPath $Disc).FullName) }
$arguments += $(if ($NoLauncher) { "--no-launcher" } else { "--launcher" })
& $Runtime @arguments
exit $LASTEXITCODE
