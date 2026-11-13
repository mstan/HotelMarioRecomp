param([string]$Version = "", [string]$Build = "build", [string]$Output = "")
$ErrorActionPreference = "Stop"
$arguments = @("-3", (Join-Path $PSScriptRoot "package.py"), "--build", $Build)
if ($Version) { $arguments += @("--version", $Version) }
if ($Output) { $arguments += @("--output", $Output) }
Push-Location (Split-Path -Parent $PSScriptRoot)
try { & py @arguments; $result = $LASTEXITCODE } finally { Pop-Location }
exit $result
