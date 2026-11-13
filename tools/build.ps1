param(
    [string]$Bios = "", [string]$Disc = "", [string]$BuildDir = "build",
    [string]$Engine = "", [string]$Generator = "Ninja", [string]$Cmake = "",
    [string]$GeneratedModules = "", [string]$ModuleSeeds = "",
    [switch]$StaticModuleEntries, [switch]$Reference, [switch]$Regenerate,
    [ValidateSet("LLE", "HLE")][string]$VideoBackend = "",
    [ValidateSet("LLE", "HLE")][string]$LoaderBackend = "",
    [ValidateSet("LLE", "HLE")][string]$DrawingBackend = "",
    [ValidateSet("LLE", "HLE")][string]$MemoryBackend = "",
    [ValidateSet("LLE", "HLE")][string]$ServiceBackend = "",
    [ValidateSet("LLE", "HLE")][string]$StreamingBackend = "",
    [ValidateSet("LLE", "HLE")][string]$BoardBackend = "",
    [ValidateSet("LLE", "HLE")][string]$GpuBackend = "",
    [ValidateRange(1,64)][int]$Jobs = 2
)
$ErrorActionPreference = "Stop"
$arguments = @("-3", (Join-Path $PSScriptRoot "build.py"), "--build-dir", $BuildDir,
    "--generator", $Generator, "--jobs", $Jobs)
foreach ($pair in @(@("bios",$Bios),@("disc",$Disc),@("engine",$Engine),@("cmake",$Cmake),
                    @("module-seeds",$ModuleSeeds),@("video-backend",$VideoBackend),
                    @("loader-backend",$LoaderBackend),@("drawing-backend",$DrawingBackend),
                    @("memory-backend",$MemoryBackend),@("service-backend",$ServiceBackend),
                    @("streaming-backend",$StreamingBackend),@("board-backend",$BoardBackend),@("gpu-backend",$GpuBackend))) {
    if ($pair[1]) { $arguments += @("--" + $pair[0], $pair[1]) }
}
if ($GeneratedModules) { throw "Use build.py --generated-dir <root> for both BIOS and modules." }
if ($StaticModuleEntries) { $arguments += "--static-module-entries" }
if ($Reference) { $arguments += "--reference" }
if ($Regenerate) { $arguments += "--regenerate" }
Push-Location (Split-Path -Parent $PSScriptRoot)
try { & py @arguments; $result = $LASTEXITCODE } finally { Pop-Location }
exit $result
