$ErrorActionPreference = "Stop"

$projectRoot = $PSScriptRoot
$frontendRoot = Join-Path $projectRoot "frontend"
$backendLog = Join-Path $projectRoot "backend.log"
$frontendLog = Join-Path $projectRoot "frontend.log"

function Write-Info($msg) {
    Write-Host "[INFO] $msg" -ForegroundColor Cyan
}

function Write-Warn($msg) {
    Write-Host "[WARN] $msg" -ForegroundColor Yellow
}

function Write-ErrorAndExit($msg) {
    Write-Host "[ERROR] $msg" -ForegroundColor Red
    exit 1
}

function Test-Command($name) {
    return $null -ne (Get-Command $name -ErrorAction SilentlyContinue)
}

function Stop-ProcessByPort($port) {
    $connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    if (-not $connections) { return }

    $pids = $connections | Select-Object -ExpandProperty OwningProcess -Unique

    foreach ($procId in $pids) {
        try {
            $proc = Get-Process -Id $procId -ErrorAction Stop
            Write-Warn "Stopping process on port ${port}: $($proc.ProcessName) (PID $pid)"
            Stop-Process -Id $pid -Force
        } catch {
            Write-Warn "Could not stop process on port ${port}: $($_.Exception.Message)"
        }
    }
}

# check project structure
if (-not (Test-Path (Join-Path $projectRoot "app"))) {
    Write-ErrorAndExit "Folder 'app' not found. Put this script in the project root."
}
if (-not (Test-Path (Join-Path $projectRoot "frontend"))) {
    Write-ErrorAndExit "Folder 'frontend' not found. Put this script in the project root."
}
if (-not (Test-Path (Join-Path $projectRoot "app\main.py"))) {
    Write-ErrorAndExit "File 'app/main.py' not found."
}
if (-not (Test-Path (Join-Path $projectRoot "frontend\package.json"))) {
    Write-ErrorAndExit "File 'frontend/package.json' not found."
}

# check tools
if (-not (Test-Command "git")) { Write-ErrorAndExit "Git not found." }
if (-not (Test-Command "python")) { Write-ErrorAndExit "Python not found." }
if (-not (Test-Command "node")) { Write-ErrorAndExit "Node.js not found." }
if (-not (Test-Command "npm")) { Write-ErrorAndExit "npm not found." }

# optional git sync
if (Test-Path (Join-Path $projectRoot ".git")) {
    Write-Info "Syncing repository..."
    try {
        Set-Location $projectRoot
        git fetch origin
        git checkout feature/cars-api 2>$null
        git pull --rebase origin feature/cars-api 2>$null
    } catch {
        Write-Warn "Could not sync Git automatically. Continuing..."
    }
} else {
    Write-Warn "No .git folder found. Skipping Git sync."
}

Stop-ProcessByPort 8000
Stop-ProcessByPort 5173

# backend venv
$venvPath = Join-Path $projectRoot ".venv"
if (-not (Test-Path $venvPath)) {
    Write-Info "Creating virtual environment..."
    python -m venv $venvPath
} else {
    Write-Info ".venv already exists."
}

$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
if (-not (Test-Path $activateScript)) {
    Write-ErrorAndExit "Could not find venv activation script."
}
. $activateScript

$requirementsFile = Join-Path $projectRoot "requirements.txt"
if (Test-Path $requirementsFile) {
    Write-Info "Installing backend requirements..."
    pip install -r $requirementsFile
} else {
    Write-Info "Installing default backend packages..."
    pip install --upgrade pip
    pip install fastapi uvicorn sqlmodel sqlalchemy
}

# frontend deps
if (-not (Test-Path (Join-Path $frontendRoot "node_modules"))) {
    Write-Info "Installing frontend dependencies..."
    Set-Location $frontendRoot
    npm install
} else {
    Write-Info "Frontend dependencies already installed."
}

# start backend
$backendCommand = @"
Set-Location '$projectRoot'
. '$activateScript'
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 2>&1 | Tee-Object -FilePath '$backendLog'
"@

Start-Process powershell -ArgumentList '-NoExit', '-Command', $backendCommand

# start frontend
$frontendCommand = @"
Set-Location '$frontendRoot'
npm run dev -- --host 0.0.0.0 2>&1 | Tee-Object -FilePath '$frontendLog'
"@

Start-Process powershell -ArgumentList '-NoExit', '-Command', $frontendCommand

# open browser
Start-Sleep -Seconds 4
Start-Process "http://localhost:5173"
#Start-Process "http://localhost:8000/docs"

Write-Host ""
Write-Host "===============================================" -ForegroundColor Green
Write-Host "Project launched successfully" -ForegroundColor Green
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Green
Write-Host "Backend API docs: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "Logs:"
Write-Host "  Backend: $backendLog" -ForegroundColor Cyan
Write-Host "  Frontend: $frontendLog" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Green