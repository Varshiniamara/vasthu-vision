# Vastu Vision - Unified Server Startup Script
# Starts all servers needed for the application

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   VASTU VISION - STARTING ALL SERVERS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start Python HTTP Server for Frontend (Port 8000)
Write-Host "[1/4] Starting Frontend Server (Port 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m http.server 8000" -WindowStyle Minimized
Start-Sleep -Seconds 2

# Start ML Analysis Server (Port 5000)
Write-Host "[2/4] Starting ML Analysis Server (Port 5000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python analyze_vastu.py" -WindowStyle Minimized
Start-Sleep -Seconds 2

# Start Image Analysis Server (Port 5001)
Write-Host "[3/4] Starting Image Analysis Server (Port 5001)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python analyze_image.py" -WindowStyle Minimized
Start-Sleep -Seconds 2

# Start Blueprint Generator Server (Port 5002)
Write-Host "[4/7] Starting Blueprint Generator Server (Port 5002)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python generate_blueprints.py" -WindowStyle Minimized
Start-Sleep -Seconds 2

# Start AI Blueprint Service (Port 5003)
Write-Host "[5/7] Starting AI Blueprint Service (Port 5003)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python ai_blueprint_service.py" -WindowStyle Minimized
Start-Sleep -Seconds 2

# Start AI Layout Suggester (Port 5004)
Write-Host "[6/7] Starting AI Layout Suggester (Port 5004)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python ai_layout_suggester.py" -WindowStyle Minimized
Start-Sleep -Seconds 2

# Start Energy Heatmap Generator (Port 5005)
Write-Host "[7/7] Starting Energy Heatmap Generator (Port 5005)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python energy_heatmap_generator.py" -WindowStyle Minimized
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   ALL SERVERS RUNNING!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend:        http://localhost:8000" -ForegroundColor White
Write-Host "ML API:          http://localhost:5000" -ForegroundColor White
Write-Host "Image API:       http://localhost:5001" -ForegroundColor White
Write-Host "Blueprint:       http://localhost:5002" -ForegroundColor White
Write-Host "AI Blueprint:    http://localhost:5003" -ForegroundColor Cyan
Write-Host "AI Layout:       http://localhost:5004" -ForegroundColor Cyan
Write-Host "Energy Heatmap:  http://localhost:5005" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   OPEN THIS URL IN YOUR BROWSER:" -ForegroundColor Cyan
Write-Host "   http://localhost:8000/index.html" -ForegroundColor Yellow -BackgroundColor DarkBlue
Write-Host ""
Write-Host "   AI Features Page:" -ForegroundColor Cyan
Write-Host "   http://localhost:8000/ai_features_page.html" -ForegroundColor Yellow -BackgroundColor DarkBlue
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Servers are running in minimized PowerShell windows." -ForegroundColor Gray
Write-Host "Close those windows to stop the servers." -ForegroundColor Gray
Write-Host ""
Write-Host "Opening browser in 3 seconds..." -ForegroundColor Cyan
Start-Sleep -Seconds 3

# Open browser
Start-Process "http://localhost:8000/index.html"

Write-Host ""
Write-Host "Press any key to exit (servers will keep running)..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

