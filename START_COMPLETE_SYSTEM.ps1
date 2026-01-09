# Vastu Vision - Complete System Startup Script
# Starts Frontend, Backend APIs, and all Python services

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   VASTU VISION - COMPLETE SYSTEM" -ForegroundColor Cyan
Write-Host "   Starting All Services..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "[CHECK] Verifying Python installation..." -ForegroundColor Yellow
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCmd) {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python not found! Please install Python first." -ForegroundColor Red
    exit 1
}

# Check and install Python dependencies
Write-Host ""
Write-Host "[SETUP] Checking Python dependencies..." -ForegroundColor Yellow
$requirementsFiles = @(
    "ml_model\requirements.txt"
)

foreach ($reqFile in $requirementsFiles) {
    if (Test-Path $reqFile) {
        Write-Host "  Installing dependencies from $reqFile..." -ForegroundColor Gray
        python -m pip install -q -r $reqFile
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Dependencies installed" -ForegroundColor Green
        } else {
            Write-Host "  ⚠ Some dependencies may have failed to install" -ForegroundColor Yellow
        }
    }
}

# Install Flask and Flask-CORS if not present (required for Python APIs)
Write-Host ""
Write-Host "[SETUP] Installing API dependencies..." -ForegroundColor Yellow
python -m pip install -q flask flask-cors matplotlib numpy pandas scikit-learn joblib
Write-Host "✓ API dependencies ready" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   STARTING ALL SERVERS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start Frontend Server (Port 8000)
Write-Host "[1/9] Starting Frontend Server (Port 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python -m http.server 8000" -WindowStyle Minimized
Start-Sleep -Seconds 2

# Start ML Analysis Server (Port 5000)
Write-Host "[2/9] Starting ML Analysis Server (Port 5000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python analyze_vastu.py" -WindowStyle Minimized
Start-Sleep -Seconds 2

# Start Image Analysis Server (Port 5001)
Write-Host "[3/9] Starting Image Analysis Server (Port 5001)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python analyze_image.py" -WindowStyle Minimized
Start-Sleep -Seconds 2

# Start Blueprint Generator Server (Port 5002)
Write-Host "[4/9] Starting Blueprint Generator Server (Port 5002)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python generate_blueprints.py" -WindowStyle Minimized
Start-Sleep -Seconds 2

# Start AI Blueprint Service (Port 5003)
Write-Host "[5/9] Starting AI Blueprint Service (Port 5003)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python ai_blueprint_service.py" -WindowStyle Minimized
Start-Sleep -Seconds 2

# Start AI Layout Suggester (Port 5004)
Write-Host "[6/9] Starting AI Layout Suggester (Port 5004)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python ai_layout_suggester.py" -WindowStyle Minimized
Start-Sleep -Seconds 2

# Start Energy Heatmap Generator (Port 5005)
Write-Host "[7/9] Starting Energy Heatmap Generator (Port 5005)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python energy_heatmap_generator.py" -WindowStyle Minimized
Start-Sleep -Seconds 2

# Start Professional Blueprint Generator (Port 5006)
Write-Host "[8/9] Starting Professional Blueprint Generator (Port 5006)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python professional_blueprint_generator.py" -WindowStyle Minimized
Start-Sleep -Seconds 2

# Start 3D Visualization Generator (Port 5007)
Write-Host "[9/9] Starting 3D Visualization Generator (Port 5007)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python 3d_visualization_generator.py" -WindowStyle Minimized
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   ✓ ALL SERVICES RUNNING!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 FRONTEND & BACKEND SERVICES:" -ForegroundColor White
Write-Host "   Frontend:           http://localhost:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "🤖 PYTHON AI/ML APIs:" -ForegroundColor White
Write-Host "   ML Analysis API:    http://localhost:5000" -ForegroundColor Cyan
Write-Host "   Image Analysis:     http://localhost:5001" -ForegroundColor Cyan
Write-Host "   Blueprint Generator: http://localhost:5002" -ForegroundColor Cyan
Write-Host "   AI Blueprint:       http://localhost:5003" -ForegroundColor Cyan
Write-Host "   AI Layout:          http://localhost:5004" -ForegroundColor Cyan
Write-Host "   Energy Heatmap:     http://localhost:5005" -ForegroundColor Cyan
Write-Host "   Professional BP:    http://localhost:5006" -ForegroundColor Cyan
Write-Host "   3D Visualization:   http://localhost:5007" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "   📱 OPEN IN BROWSER:" -ForegroundColor Yellow
Write-Host "   http://localhost:8000/index.html" -ForegroundColor White -BackgroundColor DarkBlue
Write-Host ""
Write-Host "   AI Features: http://localhost:8000/ai_features_page.html" -ForegroundColor White -BackgroundColor DarkBlue
Write-Host "   Dashboard:   http://localhost:8000/dashboard.html" -ForegroundColor White -BackgroundColor DarkBlue
Write-Host "   Results:     http://localhost:8000/results.html" -ForegroundColor White -BackgroundColor DarkBlue
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "📝 NOTE:" -ForegroundColor Gray
Write-Host "   • PHP backend files require a web server (like Hostinger)" -ForegroundColor Gray
Write-Host "   • For local testing, frontend and Python APIs are fully functional" -ForegroundColor Gray
Write-Host "   • All servers are running in minimized PowerShell windows" -ForegroundColor Gray
Write-Host "   • Close those windows to stop the servers" -ForegroundColor Gray
Write-Host ""
Write-Host "Opening browser in 3 seconds..." -ForegroundColor Cyan
Start-Sleep -Seconds 3

# Open browser
Start-Process "http://localhost:8000/index.html"

Write-Host ""
Write-Host "✓ System started successfully!" -ForegroundColor Green
Write-Host "Press any key to exit (servers will keep running)..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

