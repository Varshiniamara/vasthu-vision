#!/bin/bash

# Ensure we are in the correct directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"
echo "📂 Working Directory: $DIR"

# Kill existing processes
echo "🛑 Stopping existing services..."
pkill -f "python -m http.server"
pkill -f "php -S"
pkill -f "analyze_vastu.py"
pkill -f "analyze_image.py"
pkill -f "generate_blueprints.py"
pkill -f "geospatial_service.py"
pkill -f "analyze_video_vastu.py"

# Double check port 8000 is free
lsof -ti:8000 | xargs kill -9 >/dev/null 2>&1

sleep 2

echo "==============================================="
echo "🚀 RESTARTING VASTUVISION XR PLATFORM"
echo "==============================================="

# 1. Start Web Server (Prefer PHP for compatibility, fallback to Python)
# We strictly bind to this directory
if command -v php >/dev/null 2>&1; then
    echo "🌐 Starting PHP Web Server (Port 8000)..."
    php -S 0.0.0.0:8000 -t . > /dev/null 2>&1 &
else
    echo "⚠️ PHP not found! Using Python Web Server."
    python3 -m http.server 8000 > /dev/null 2>&1 &
fi

# 2. Start Backend Services
echo "🧠 Starting Vastu Analysis Engine (Port 5000)..."
python3 analyze_vastu.py > /dev/null 2>&1 &

echo "👁️ Starting Image Analysis Engine (Port 5001)..."
python3 analyze_image.py > /dev/null 2>&1 &

echo "🏗️ Starting Blueprint Generator (Port 5002)..."
python3 generate_blueprints.py > /dev/null 2>&1 &

echo "🌍 Starting Geospatial Intelligence (Port 5006)..."
python3 geospatial_service.py > /dev/null 2>&1 &

echo "📹 Starting AR/Video Analysis (Port 5007)..."
python3 analyze_video_vastu.py > /dev/null 2>&1 &

echo "==============================================="
echo "✅ SYSTEM REBOOTED"
echo "==============================================="
echo "Please refresh your browser:"
echo "👉 http://localhost:8000/xr_ar_vr.html"
echo "==============================================="
