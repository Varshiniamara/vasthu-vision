@echo off
chcp 65001 >nul
echo ========================================
echo   VASTU VISION - COMPLETE SYSTEM
echo   Starting Everything...
echo ========================================
echo.

echo [CHECK] Verifying Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python first.
    pause
    exit /b 1
)
python --version
echo.

echo [SETUP] Installing Python dependencies...
echo   Installing ML model dependencies...
if exist ml_model\requirements.txt (
    python -m pip install -q -r ml_model\requirements.txt
)
echo   Installing API dependencies...
python -m pip install -q flask flask-cors matplotlib numpy pandas scikit-learn joblib
echo   [OK] Dependencies ready
echo.

echo ========================================
echo   STARTING ALL SERVERS
echo ========================================
echo.

echo [1/9] Starting Frontend Server (Port 8000)...
start "Frontend Server" cmd /k "python -m http.server 8000"
timeout /t 2 /nobreak >nul

echo [2/9] Starting ML Analysis Server (Port 5000)...
start "ML Analysis Server" cmd /k "python analyze_vastu.py"
timeout /t 2 /nobreak >nul

echo [3/9] Starting Image Analysis Server (Port 5001)...
start "Image Analysis Server" cmd /k "python analyze_image.py"
timeout /t 2 /nobreak >nul

echo [4/9] Starting Blueprint Generator Server (Port 5002)...
start "Blueprint Generator Server" cmd /k "python generate_blueprints.py"
timeout /t 2 /nobreak >nul

echo [5/9] Starting AI Blueprint Service (Port 5003)...
start "AI Blueprint Service" cmd /k "python ai_blueprint_service.py"
timeout /t 2 /nobreak >nul

echo [6/9] Starting AI Layout Suggester (Port 5004)...
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
timeout /t 2 /nobreak >nul

echo [10/10] Starting AI Assistant Service (Port 5008)...
start "AI Assistant Service" cmd /k "python ai_assistant_service.py"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo   ALL SERVICES RUNNING!
echo ========================================
echo.
echo FRONTEND ^& BACKEND SERVICES:
echo   Frontend:           http://localhost:8000
echo.
echo PYTHON AI/ML APIs:
echo   ML Analysis API:    http://localhost:5000
echo   Image Analysis:     http://localhost:5001
echo   Blueprint Generator: http://localhost:5002
echo   AI Blueprint:       http://localhost:5003
echo   AI Layout:          http://localhost:5004
echo   Energy Heatmap:     http://localhost:5005
echo   Professional BP:    http://localhost:5006
echo   3D Visualization:   http://localhost:5007
echo   AI Assistant:        http://localhost:5008
echo.
echo ========================================
echo   OPEN IN BROWSER:
echo   http://localhost:8000/index.html
echo.
echo   AI Chat Interface:  http://localhost:8000/ai_chat.html
echo.
echo   AI Features: http://localhost:8000/ai_features_page.html
echo   Dashboard:   http://localhost:8000/dashboard.html
echo   Results:     http://localhost:8000/results.html
echo ========================================
echo.
echo NOTE:
echo   - PHP backend files require a web server (like Hostinger)
echo   - For local testing, frontend and Python APIs are fully functional
echo   - All servers are running in separate windows
echo   - Close those windows to stop the servers
echo.
echo Opening browser in 3 seconds...
timeout /t 3 /nobreak >nul
start http://localhost:8000/index.html
echo.
echo System started successfully!
pause

