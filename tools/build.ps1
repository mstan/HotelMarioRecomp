param(
    [string]$BuildDir = "build",
    [string]$Engine = "",
    [string]$Generator = "Ninja",
    [string]$Disc = "",
    [string]$GeneratedModules = "",
    [string]$Cmake = "",
    [string]$ModuleSeeds = ""
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
if (-not $Engine) {
    $Engine = Join-Path (Split-Path -Parent $root) "cdirecomp"
}
$cmakeCommand = $Cmake
$mingwCmake = "C:/msys64/mingw64/bin/cmake.exe"
$windowsCmake = "C:/Program Files/Microsoft Visual Studio/2022/Community/Common7/IDE/CommonExtensions/Microsoft/CMake/CMake/bin/cmake.exe"
if (-not $cmakeCommand -and (Test-Path -LiteralPath $mingwCmake)) {
    $cmakeCommand = $mingwCmake
}
if (-not $cmakeCommand -and (Test-Path -LiteralPath $windowsCmake)) {
    $cmakeCommand = $windowsCmake
}
if (-not $cmakeCommand) { $cmakeCommand = (Get-Command cmake -ErrorAction Stop).Source }
$Engine = (Get-Item -LiteralPath $Engine).FullName
if (-not $GeneratedModules) { $GeneratedModules = Join-Path $Engine "hotelmario/generated" }
if ($Disc) {
    $Disc = (Get-Item -LiteralPath $Disc).FullName
    $toolBuild = Join-Path $Engine "build/recompiler"
    & $cmakeCommand -S (Join-Path $Engine "recompiler") -B $toolBuild -G $Generator -DCMAKE_BUILD_TYPE=Release
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    & $cmakeCommand --build $toolBuild --config Release --target CdiRecomp -j 4
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    $recompiler = Join-Path $toolBuild "CdiRecomp.exe"
    if (-not (Test-Path -LiteralPath $recompiler)) { $recompiler = Join-Path $toolBuild "Release/CdiRecomp.exe" }
    $emitArguments = @($Disc, "--emit", "--out", $GeneratedModules, "--subr-exports", "named-offset32")
    if ($ModuleSeeds) { $emitArguments += @("--module-seeds", (Get-Item -LiteralPath $ModuleSeeds).FullName) }
    & $recompiler @emitArguments
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

Push-Location $root
try {
    & $cmakeCommand -S . -B $BuildDir -G $Generator `
        -DCMAKE_BUILD_TYPE=Release `
        "-DCDIRECOMP_ROOT=$Engine" "-DCDI_GAME_GENERATED_DIR=$GeneratedModules"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    & $cmakeCommand --build $BuildDir --config Release -j
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
