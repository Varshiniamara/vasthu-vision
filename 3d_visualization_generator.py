#!/usr/bin/env python3
"""
3D Visualization Generator for Vastu Floor Plans
Creates 3D models with dimensions and directions
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Polygon
import numpy as np
import io
import base64
import json
from typing import Dict, Any

app = Flask(__name__)
CORS(app)

# Vastu Zone Colors
ZONE_COLORS = {
    'northeast': '#4ECDC4',  # Water - Light blue
    'north': '#7ED321',       # Air - Green
    'northwest': '#50E3C2',   # Air - Cyan
    'east': '#B8E986',        # Air - Light green
    'southeast': '#FF6B6B',   # Fire - Red
    'south': '#F5A623',       # Fire - Orange
    'southwest': '#9013FE',   # Earth - Purple
    'west': '#E9C46A',        # Fire/Air - Yellow
    'center': '#AA96DA'       # Space - Lavender
}

def create_3d_floor_plan(space_data: Dict[str, Any]) -> str:
    """Create 3D visualization of floor plan"""
    
    plot_size = space_data.get('plotSize', '1200 sq ft')
    rooms = space_data.get('rooms', [])
    orientation = space_data.get('orientation', 'north-facing')
    
    # Calculate plot dimensions
    try:
        plot_area = int(''.join(filter(str.isdigit, plot_size)))
    except:
        plot_area = 1200
    
    if plot_area <= 1200:
        plot_width, plot_height = 30, 40
    elif plot_area <= 2000:
        plot_width, plot_height = 35, 50
    elif plot_area <= 2800:
        plot_width, plot_height = 40, 60
    else:
        plot_width, plot_height = 50, 70
    
    # Create 3D figure
    fig = plt.figure(figsize=(20, 20))
    ax = fig.add_subplot(111, projection='3d')
    
    # Set axis limits
    ax.set_xlim(0, plot_width)
    ax.set_ylim(0, plot_height)
    ax.set_zlim(0, 15)
    
    # Room height
    room_height = 10
    
    # Process rooms
    room_positions = {}
    for room in rooms:
        room_name = room.get('name', '').lower()
        room_zone = room.get('zone', '').lower()
        
        # Calculate position based on zone
        if room_zone == 'northeast':
            x, y = plot_width * 0.7, plot_height * 0.7
            w, h = plot_width * 0.3, plot_height * 0.3
        elif room_zone == 'southeast':
            x, y = plot_width * 0.7, plot_height * 0.1
            w, h = plot_width * 0.3, plot_height * 0.3
        elif room_zone == 'southwest':
            x, y = plot_width * 0.1, plot_height * 0.1
            w, h = plot_width * 0.3, plot_height * 0.3
        elif room_zone == 'northwest':
            x, y = plot_width * 0.1, plot_height * 0.7
            w, h = plot_width * 0.3, plot_height * 0.3
        elif room_zone == 'north':
            x, y = plot_width * 0.4, plot_height * 0.7
            w, h = plot_width * 0.3, plot_height * 0.2
        elif room_zone == 'south':
            x, y = plot_width * 0.4, plot_height * 0.1
            w, h = plot_width * 0.3, plot_height * 0.2
        elif room_zone == 'east':
            x, y = plot_width * 0.7, plot_height * 0.4
            w, h = plot_width * 0.2, plot_height * 0.3
        elif room_zone == 'west':
            x, y = plot_width * 0.1, plot_height * 0.4
            w, h = plot_width * 0.2, plot_height * 0.3
        else:  # center
            x, y = plot_width * 0.35, plot_height * 0.35
            w, h = plot_width * 0.3, plot_height * 0.3
        
        room_positions[room_name] = {
            'x': x, 'y': y, 'width': w, 'height': h,
            'zone': room_zone, 'name': room.get('name', 'Room')
        }
    
    # Add default rooms
    default_rooms = [
        {'name': 'Kitchen', 'zone': 'southeast', 'x': plot_width*0.65, 'y': plot_height*0.1, 
         'width': plot_width*0.25, 'height': plot_height*0.25},
        {'name': 'Bedroom', 'zone': 'southwest', 'x': plot_width*0.1, 'y': plot_height*0.1,
         'width': plot_width*0.3, 'height': plot_height*0.3},
        {'name': 'Living Room', 'zone': 'northeast', 'x': plot_width*0.65, 'y': plot_height*0.65,
         'width': plot_width*0.3, 'height': plot_height*0.3},
        {'name': 'Bathroom', 'zone': 'northwest', 'x': plot_width*0.1, 'y': plot_height*0.65,
         'width': plot_width*0.25, 'height': plot_height*0.25}
    ]
    
    for default_room in default_rooms:
        if default_room['name'].lower() not in room_positions:
            room_positions[default_room['name'].lower()] = {
                'x': default_room['x'], 'y': default_room['y'],
                'width': default_room['width'], 'height': default_room['height'],
                'zone': default_room['zone'], 'name': default_room['name']
            }
    
    # Draw 3D rooms
    for room_name, room_data in room_positions.items():
        x, y = room_data['x'], room_data['y']
        w, h = room_data['width'], room_data['height']
        zone = room_data['zone']
        color = ZONE_COLORS.get(zone, '#CCCCCC')
        
        # Create 3D box (walls)
        # Bottom
        ax.plot([x, x+w, x+w, x, x], [y, y, y+h, y+h, y], 
               [0, 0, 0, 0, 0], color=color, linewidth=2)
        
        # Top
        ax.plot([x, x+w, x+w, x, x], [y, y, y+h, y+h, y], 
               [room_height, room_height, room_height, room_height, room_height], 
               color=color, linewidth=2)
        
        # Vertical edges
        ax.plot([x, x], [y, y], [0, room_height], color=color, linewidth=2)
        ax.plot([x+w, x+w], [y, y], [0, room_height], color=color, linewidth=2)
        ax.plot([x+w, x+w], [y+h, y+h], [0, room_height], color=color, linewidth=2)
        ax.plot([x, x], [y+h, y+h], [0, room_height], color=color, linewidth=2)
        
        # Filled faces for better visualization
        # Top face
        top_face = np.array([[x, y, room_height], [x+w, y, room_height], 
                           [x+w, y+h, room_height], [x, y+h, room_height]])
        ax.plot_trisurf(top_face[:, 0], top_face[:, 1], top_face[:, 2], 
                       color=color, alpha=0.3)
        
        # Room label
        center_x = x + w/2
        center_y = y + h/2
        ax.text(center_x, center_y, room_height + 1, room_data['name'],
               fontsize=10, fontweight='bold', ha='center')
        
        # Dimensions label
        dim_text = f"{int(w)}'×{int(h)}'"
        ax.text(center_x, center_y, room_height + 0.5, dim_text,
               fontsize=8, ha='center', style='italic')
    
    # Plot boundary
    ax.plot([0, plot_width, plot_width, 0, 0], 
           [0, 0, plot_height, plot_height, 0],
           [0, 0, 0, 0, 0], 'k-', linewidth=3)
    
    # Compass indicator
    compass_x = plot_width * 0.9
    compass_y = plot_height * 0.9
    # North arrow
    ax.plot([compass_x, compass_x], [compass_y, compass_y + 3], [0, 0],
           'r-', linewidth=3)
    ax.text(compass_x, compass_y + 4, 0, 'N', fontsize=14, fontweight='bold',
           color='red', ha='center')
    
    # Title
    ax.text(plot_width/2, plot_height/2, room_height + 5,
           f"3D FLOOR PLAN - {orientation.upper()}",
           fontsize=16, fontweight='bold', ha='center')
    
    # Overall dimensions
    ax.text(plot_width/2, -2, 2,
           f"Overall: {plot_width}' × {plot_height}' ({plot_area} sq ft)",
           fontsize=12, ha='center', style='italic')
    
    # Set labels
    ax.set_xlabel('Width (ft)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Length (ft)', fontsize=12, fontweight='bold')
    ax.set_zlabel('Height (ft)', fontsize=12, fontweight='bold')
    
    # Set viewing angle
    ax.view_init(elev=30, azim=45)
    
    plt.tight_layout()
    
    # Save
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=200, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    plt.close()
    
    return base64.b64encode(buf.read()).decode('utf-8')

@app.route('/generate_3d_visualization', methods=['POST', 'OPTIONS'])
def generate_3d_visualization_endpoint():
    """Generate 3D visualization"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        print("🎨 Generating 3D visualization...")
        
        visualization_image = create_3d_floor_plan(data)
        
        return jsonify({
            'success': True,
            'image': visualization_image,
            'type': '3d_visualization'
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'service': '3d_visualization_generator'
    })

if __name__ == '__main__':
    print("=" * 70)
    print("🎨 VASTU VISION - 3D VISUALIZATION GENERATOR")
    print("=" * 70)
    print("✅ 3D floor plan visualization")
    print("✅ Dimensions and directions")
    print("✅ Color-coded zones")
    print("🌐 Server: http://localhost:5007")
    print("=" * 70)
    app.run(host='0.0.0.0', port=5007, debug=True)

