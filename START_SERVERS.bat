@echo off
echo ========================================
echo   VASTU VISION - STARTING ALL SERVERS
echo ========================================
echo.

echo [1/4] Starting Frontend Server (Port 8000)...
start "Frontend Server" cmd /k "python -m http.server 8000"
timeout /t 2 /nobreak >nul

echo [2/4] Starting ML Analysis Server (Port 5000)...
start "ML Analysis Server" cmd /k "python analyze_vastu.py"
timeout /t 2 /nobreak >nul

echo [3/4] Starting Image Analysis Server (Port 5001)...
start "Image Analysis Server" cmd /k "python analyze_image.py"
timeout /t 2 /nobreak >nul

echo [4/7] Starting Blueprint Generator Server (Port 5002)...
start "Blueprint Generator Server" cmd /k "python generate_blueprints.py"
timeout /t 2 /nobreak >nul

echo [5/7] Starting AI Blueprint Service (Port 5003)...
start "AI Blueprint Service" cmd /k "python ai_blueprint_service.py"
timeout /t 2 /nobreak >nul

echo [6/7] Starting AI Layout Suggester (Port 5004)...
start "AI Layout Suggester" cmd /k "python ai_layout_suggester.py"
timeout /t 2 /nobreak >nul

echo [7/9] Starting Energy Heatmap Generator (Port 5005)...
start "Energy Heatmap Generator" cmd /k "python energy_heatmap_generator.py"
timeout /t 2 /nobreak >nul

echo [8/9] Starting Professional Blueprint Generator (Port 5006)...
start "Professional Blueprint Generator" cmd /k "python professional_blueprint_generator.py"
timeout /t 2 /nobreak >nul

echo [9/9] Starting 3D Visualization Generator (Port 5007)...
start "3D Visualization Generator" cmd /k "python 3d_visualization_generator.py"
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   ALL SERVERS RUNNING!
echo ========================================
echo.
echo Frontend:        http://localhost:8000
echo ML API:          http://localhost:5000
echo Image API:       http://localhost:5001
echo Blueprint:       http://localhost:5002
echo AI Blueprint:    http://localhost:5003
echo AI Layout:       http://localhost:5004
echo Energy Heatmap:  http://localhost:5005
echo Professional BP:  http://localhost:5006
echo 3D Visualization: http://localhost:5007
echo.
echo ========================================
echo   OPEN THIS URL IN YOUR BROWSER:
echo   http://localhost:8000/index.html
echo.
echo AI Features Page: http://localhost:8000/ai_features_page.html
echo ========================================
echo.
echo Servers are running in separate windows.
echo Close those windows to stop the servers.
echo.
echo Opening browser in 3 seconds...
timeout /t 3 /nobreak >nul

start http://localhost:8000/index.html

echo.
pause
