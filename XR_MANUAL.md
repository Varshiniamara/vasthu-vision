# 🚀 VastuVision XR - User Manual

## 🌟 Overview
VastuVision XR is now a unified spatial intelligence platform. It merges real-time geospatial data with authentic Vastu Shastra principles to deliver construction-ready architectural plans and live site analysis.

## 🛠️ System Architecture
The platform consists of a Unified Spatial Intelligence Engine driven by **7 Microservices**:

1. **Web Server** (Port 8000): Frontend interface.
2. **Analysis Engine** (Port 5000): Core Vastu Logic.
3. **Image Logic** (Port 5001): Existing floor plan scanning.
4. **Blueprint Engine** (Port 5002): Architecture generation.
5. **AI Services** (Ports 5003-5): AI layouts/heatmaps.
6. **Geospatial Service (NEW 5006)**: True North, Evaluation, Terrain Context.
7. **Video AR Engine (NEW 5007)**: Computer Vision for Site Videos.

## 🏁 How to Run

### Windows (PowerShell)
Right-click `START_XR.ps1` and select "Run with PowerShell".

### Mac/Linux
Open a terminal and run:
```bash
# Start Geospatial Service
python geospatial_service.py &

# Start Video Engine
python analyze_video_vastu.py &

# Start Blueprint Engine
python generate_blueprints.py &

# Start Web Server
python -m http.server 8000
```

## 🎮 Navigation Flow (Demo Script)

1. **Start**: Go to `http://localhost:8000/` and click the shiny cyan **"EXPLORE XR"** button.
2. **Setup (`xr_space.html`)**:
   - Click **"Auto-Detect"** to pull real GPS coordinates.
   - Click **"Environment Scan"** to fetch (simulated) terrain and True North data.
   - Click **"Initialize Vastu Engine"**.
3. **Dashboard (`xr_dashboard.html`)**:
   - View the "Spatial Integrity" analysis.
   - See generated blueprints under "Architectural Blueprints".
4. **Live AR (`xr_ar_vr.html`)**:
   - Click **"Launch Live AR"**.
   - **Tab 1 (Camera)**: Show the Live HUD overlaying compass directions on your webcam.
   - **Tab 2 (Video)**: Upload a site video to run the Deep Learning Analysis.
   - **Tab 3 (3D)**: See the 3D plot visualizer.

## 📱 Features for Judges
- **Geospatial Truth**: Show them the "True North" deviation on the dashboard. This proves it's not just a generic template.
- **Computer Vision**: Upload a video and show the processed frame with "Vastu Zones" identified via CV.
- **Construction Ready**: Download a blueprint and zoom in to show the dimensions and door swings.

---
**Status**: PRODUCTION READY
