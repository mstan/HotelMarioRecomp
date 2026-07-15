param(
    [string]$Bios = "",
    [string]$Disc = "",
    [string]$Runtime = ""
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$biosConfig = Join-Path $root "bios.cfg"
$discConfig = Join-Path $root "disc.cfg"

function Read-SavedPath([string]$Path) {
    if (Test-Path -LiteralPath $Path) {
        return ([IO.File]::ReadAllText($Path)).Trim()
    }
    return ""
}

function Pick-Asset([string]$Title, [string]$Filter) {
    if (-not $IsWindows -and $PSVersionTable.PSEdition -eq "Core") {
        throw "$Title is required; pass its path explicitly."
    }
    Add-Type -AssemblyName System.Windows.Forms
    $dialog = New-Object System.Windows.Forms.OpenFileDialog
    $dialog.Title = $Title
    $dialog.Filter = $Filter
    if ($dialog.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) {
        throw "$Title was not selected."
    }
    return $dialog.FileName
}

if (-not $Bios) { $Bios = Read-SavedPath $biosConfig }
if (-not $Disc) { $Disc = Read-SavedPath $discConfig }
if (-not $Bios -or -not (Test-Path -LiteralPath $Bios)) {
    $Bios = Pick-Asset "Select your CD-i BIOS" "CD-i BIOS (*.rom;*.bin)|*.rom;*.bin|All files (*.*)|*.*"
}
if (-not $Disc -or -not (Test-Path -LiteralPath $Disc)) {
    $Disc = Pick-Asset "Select your Hotel Mario disc CUE" "CD-i disc (*.cue;*.bin)|*.cue;*.bin|All files (*.*)|*.*"
}

if ((Get-Item -LiteralPath $Bios).Length -ne 524288) {
    throw "The selected BIOS must be exactly 524,288 bytes."
}
if ([IO.Path]::GetExtension($Disc).ToLowerInvariant() -notin ".cue", ".bin") {
    throw "Select a raw Mode-2 Hotel Mario .cue or .bin image (the .cue is preferred)."
}

[IO.File]::WriteAllText($biosConfig, ([IO.Path]::GetFullPath($Bios) + [Environment]::NewLine))
[IO.File]::WriteAllText($discConfig, ([IO.Path]::GetFullPath($Disc) + [Environment]::NewLine))

if (-not $Runtime) {
    $Runtime = Join-Path $root "build/HotelMarioRecomp.exe"
}
if (-not (Test-Path -LiteralPath $Runtime)) {
    throw "HotelMarioRecomp is not built at $Runtime. Run tools/build.ps1 first."
}

& $Runtime $Bios --disc $Disc
exit $LASTEXITCODE

