# Quick Start Script for Siemens Energy API Testing Framework
# Run this script for first-time setup

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Siemens Energy API Testing Framework" -ForegroundColor Cyan
Write-Host "Quick Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if command exists
function Test-CommandExists {
    param($command)
    $null = Get-Command $command -ErrorAction SilentlyContinue
    return $?
}

# Step 1: Check Prerequisites
Write-Host "[1/8] Checking prerequisites..." -ForegroundColor Yellow

$python_installed = Test-CommandExists "python"
$docker_installed = Test-CommandExists "docker"
$git_installed = Test-CommandExists "git"

if (-not $python_installed) {
    Write-Host "  ❌ Python not found. Please install Python 3.9+" -ForegroundColor Red
    exit 1
}

$python_version = python --version
Write-Host "  ✅ Python installed: $python_version" -ForegroundColor Green

if (-not $docker_installed) {
    Write-Host "  ⚠️  Docker not found. Optional but recommended." -ForegroundColor Yellow
} else {
    Write-Host "  ✅ Docker installed" -ForegroundColor Green
}

if (-not $git_installed) {
    Write-Host "  ❌ Git not found. Please install Git" -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ Git installed" -ForegroundColor Green
Write-Host ""

# Step 2: Create Virtual Environment
Write-Host "[2/8] Creating virtual environment..." -ForegroundColor Yellow

if (Test-Path "venv") {
    Write-Host "  ⚠️  Virtual environment already exists. Skipping..." -ForegroundColor Yellow
} else {
    python -m venv venv
    if ($?) {
        Write-Host "  ✅ Virtual environment created" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}
Write-Host ""

# Step 3: Activate Virtual Environment
Write-Host "[3/8] Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1
if ($?) {
    Write-Host "  ✅ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "  ❌ Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 4: Upgrade pip
Write-Host "[4/8] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
if ($?) {
    Write-Host "  ✅ Pip upgraded" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Failed to upgrade pip" -ForegroundColor Yellow
}
Write-Host ""

# Step 5: Install Dependencies
Write-Host "[5/8] Installing dependencies..." -ForegroundColor Yellow
Write-Host "  This may take a few minutes..." -ForegroundColor Gray

pip install -r requirements.txt --quiet
if (-not $?) {
    Write-Host "  ❌ Failed to install main dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ Main dependencies installed" -ForegroundColor Green

pip install -r requirements-test.txt --quiet
if (-not $?) {
    Write-Host "  ⚠️  Failed to install test dependencies" -ForegroundColor Yellow
} else {
    Write-Host "  ✅ Test dependencies installed" -ForegroundColor Green
}
Write-Host ""

# Step 6: Setup Configuration
Write-Host "[6/8] Setting up configuration..." -ForegroundColor Yellow

if (-not (Test-Path "config\dev.env")) {
    if (Test-Path "config\.env.template") {
        Copy-Item "config\.env.template" "config\dev.env"
        Write-Host "  ✅ Created config\dev.env from template" -ForegroundColor Green
        Write-Host "  ⚠️  Please edit config\dev.env with your settings!" -ForegroundColor Yellow
    } else {
        Write-Host "  ⚠️  Template not found. Please create config\dev.env manually" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ✅ Configuration file already exists" -ForegroundColor Green
}
Write-Host ""

# Step 7: Create Directories
Write-Host "[7/8] Creating directories..." -ForegroundColor Yellow

$directories = @("logs", "reports", "allure-results", "allure-report")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  ✅ Created $dir/" -ForegroundColor Green
    }
}
Write-Host ""

# Step 8: Start Database (if Docker is available)
Write-Host "[8/8] Starting database..." -ForegroundColor Yellow

if ($docker_installed) {
    $docker_running = docker ps 2>$null
    if ($?) {
        Write-Host "  Starting PostgreSQL container..." -ForegroundColor Gray
        docker-compose up -d postgres
        
        if ($?) {
            Write-Host "  ✅ PostgreSQL started" -ForegroundColor Green
            Write-Host "  Waiting for database to be ready..." -ForegroundColor Gray
            Start-Sleep -Seconds 5
        } else {
            Write-Host "  ⚠️  Failed to start PostgreSQL. Check docker-compose.yml" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  ⚠️  Docker is not running. Please start Docker Desktop" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ⚠️  Docker not available. Please start PostgreSQL manually" -ForegroundColor Yellow
}
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete! 🎉" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Edit config\dev.env with your settings" -ForegroundColor White
Write-Host "  2. Run database migrations: alembic upgrade head" -ForegroundColor White
Write-Host "  3. Run tests: pytest tests/ -v" -ForegroundColor White
Write-Host "  4. Or use test runner: python run_tests.py --all" -ForegroundColor White
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Yellow
Write-Host "  • README.md - Project overview" -ForegroundColor White
Write-Host "  • FRAMEWORK_SETUP_GUIDE.md - Detailed setup" -ForegroundColor White
Write-Host "  • DEVOPS_INTEGRATION.md - CI/CD setup" -ForegroundColor White
Write-Host "  • TEST_COMMANDS.md - Test command reference" -ForegroundColor White
Write-Host ""
Write-Host "Quick Commands:" -ForegroundColor Yellow
Write-Host "  • Run all tests: python run_tests.py --all" -ForegroundColor White
Write-Host "  • Run with coverage: python run_tests.py --all --coverage" -ForegroundColor White
Write-Host "  • Run smoke tests: python run_tests.py --markers smoke" -ForegroundColor White
Write-Host "  • Run in parallel: python run_tests.py --all --parallel" -ForegroundColor White
Write-Host ""
Write-Host "For help: python run_tests.py --help" -ForegroundColor Gray
Write-Host ""
Write-Host "Happy Testing! 🚀" -ForegroundColor Cyan
