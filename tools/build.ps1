param(
    [string]$BuildDir = "build",
    [string]$Engine = "",
    [string]$Generator = "Ninja"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
if (-not $Engine) {
    $Engine = Join-Path (Split-Path -Parent $root) "cdirecomp"
}
$engineArgument = $Engine
$cmakeCommand = "cmake"
$windowsCmake = "C:/Program Files/Microsoft Visual Studio/2022/Community/Common7/IDE/CommonExtensions/Microsoft/CMake/CMake/bin/cmake.exe"
if (Test-Path -LiteralPath $windowsCmake) {
    $cmakeCommand = $windowsCmake
}

Push-Location $root
try {
    & $cmakeCommand -S . -B $BuildDir -G $Generator `
        -DCMAKE_BUILD_TYPE=Release `
        "-DCDIRECOMP_ROOT=$engineArgument"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    & $cmakeCommand --build $BuildDir --config Release -j
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
