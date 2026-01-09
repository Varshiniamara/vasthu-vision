$currentDir = Get-Location

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "🚀 STARTING VASTU VISION XR - UNIFIED ENGINE" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

# 1. Frontend Server
Write-Host "🌐 Starting Web Server (Port 8000)..." -ForegroundColor Green
Start-Process python -ArgumentList "-m http.server 8000" -WindowStyle Minimized

# 2. Original Vastu Backend
Write-Host "🧠 Starting Vastu Analysis Engine (Port 5000)..." -ForegroundColor Green
Start-Process python -ArgumentList "analyze_vastu.py" -WindowStyle Minimized

# 3. Image Analysis Backend
Write-Host "👁️ Starting Image Analysis Engine (Port 5001)..." -ForegroundColor Green
Start-Process python -ArgumentList "analyze_image.py" -WindowStyle Minimized

# 4. Blueprint Generator
Write-Host "🏗️ Starting Blueprint Generator (Port 5002)..." -ForegroundColor Green
Start-Process python -ArgumentList "generate_blueprints.py" -WindowStyle Minimized

# 5. New Geospatial Intelligence
Write-Host "🌍 Starting Geospatial Intelligence (Port 5006)..." -ForegroundColor Magenta
Start-Process python -ArgumentList "geospatial_service.py" -WindowStyle Minimized

# 6. New Video/AR Analysis
Write-Host "📹 Starting AR/Video Analysis (Port 5007)..." -ForegroundColor Magenta
Start-Process python -ArgumentList "analyze_video_vastu.py" -WindowStyle Minimized

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "✅ SYSTEM ONLINE - XR FEATURES ENABLED" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "POINT OF ENTRY:"
Write-Host "👉 http://localhost:8000/xr_space.html" -ForegroundColor Yellow
Write-Host "==============================================="
Write-Host "Press any key to stop all servers..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Stop-Process -Name "python" -ErrorAction SilentlyContinue
Write-Host "🛑 All servers stopped." -ForegroundColor Red
