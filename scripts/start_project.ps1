param(
    [switch]$NoBackend,
    [switch]$NoFrontend
)

$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$venvPython = Join-Path $repoRoot '.venv\Scripts\python.exe'
$frontendDir = Join-Path $repoRoot 'frontend'

if (-not (Test-Path $venvPython)) {
    throw "Python virtual environment not found at $venvPython. Run: python -m venv .venv"
}

if (-not $NoBackend) {
    $backendCommand = @(
        '-NoExit',
        '-Command',
        "Set-Location '$repoRoot'; `$env:PYTHONPATH='$repoRoot'; & '$venvPython' -m backend.app"
    )

    Write-Host "Starting backend..."
    Start-Process powershell @backendCommand
}

if (-not $NoFrontend) {
    $frontendCommand = @(
        '-NoExit',
        '-Command',
        "Set-Location '$frontendDir'; npm run dev -- --host 0.0.0.0"
    )

    Write-Host "Starting frontend..."
    Start-Process powershell @frontendCommand
}

Write-Host ""
Write-Host "Project startup launched."
Write-Host "Backend: http://localhost:5000"
Write-Host "Frontend: http://localhost:5173"
Write-Host ""
Write-Host "Use Ctrl+C in the terminal windows to stop the services."
