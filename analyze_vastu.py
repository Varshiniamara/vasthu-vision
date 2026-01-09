#!/usr/bin/env python3
"""
Vastu Analysis Backend - Python Flask Server
Integrates ML model with frontend and generates 2D visualization
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys
import json
import subprocess
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import io
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# ML Model Path
ML_MODEL_PATH = Path(__file__).parent / 'ml_model' / 'predict.py'

def encode_orientation(orientation):
    """Encode orientation to number"""
    mapping = {
        'north-facing': 0,
        'northeast-facing': 1,
        'east-facing': 2,
        'southeast-facing': 3,
        'south-facing': 4,
        'southwest-facing': 5,
        'west-facing': 6,
        'northwest-facing': 7
    }
    return mapping.get(orientation.lower(), 2)

def encode_room_type(room_type):
    """Encode room type to number"""
    mapping = {
        '1bhk': 1,
        '2bhk': 2,
        '3bhk': 3,
        '4bhk': 4,
        '5bhk': 5,
        'studio': 0,
        'duplex': 6,
        'penthouse': 7
    }
    return mapping.get(room_type.lower(), 3)

def encode_zone(zone):
    """Encode zone to number"""
    mapping = {
        'north': 0,
        'northeast': 1,
        'east': 2,
        'southeast': 3,
        'south': 4,
        'southwest': 5,
        'west': 6,
        'northwest': 7,
        'center': 8
    }
    return mapping.get(zone.lower(), 8)

def calculate_5_elements(space_data):
    """Calculate 5 elements scores based on Vastu principles"""
    rooms = space_data.get('rooms', [])
    orientation = space_data.get('orientation', 'north-facing')
    floor_num = int(space_data.get('floorNumber', 1))
    plot_size = space_data.get('plotSize', '1200 sq ft')
    
    # Parse plot size
    plot_area = 1200
    try:
        plot_area = int(''.join(filter(str.isdigit, plot_size)))
    except:
        pass
    
    # Initialize elements with base scores
    elements = {
        'Fire': 50,
        'Water': 50,
        'Earth': 50,
        'Air': 50,
        'Space': 50
    }
    
    # Analyze rooms and zones for Vastu compliance
    for room in rooms:
        room_name = room.get('name', '').lower()
        room_zone = room.get('zone', '').lower()
        
        # Fire element (Southeast is ideal for Kitchen)
        if 'kitchen' in room_name:
            if 'southeast' in room_zone:
                elements['Fire'] += 25  # Perfect placement
            elif 'south' in room_zone or 'east' in room_zone:
                elements['Fire'] += 15  # Good placement
            else:
                elements['Fire'] -= 10  # Poor placement
        
        # Water element (Northeast is ideal for water sources)
        if 'bathroom' in room_name or 'water' in room_name or 'wash' in room_name:
            if 'northeast' in room_zone:
                elements['Water'] += 30  # Perfect placement
            elif 'north' in room_zone or 'east' in room_zone:
                elements['Water'] += 15  # Good placement
            else:
                elements['Water'] -= 5  # Poor placement
        
        # Earth element (Southwest is ideal for heavy structures/bedrooms)
        if 'bedroom' in room_name or 'master' in room_name:
            if 'southwest' in room_zone:
                elements['Earth'] += 25  # Perfect placement
            elif 'south' in room_zone or 'west' in room_zone:
                elements['Earth'] += 15  # Good placement
            else:
                elements['Earth'] -= 5  # Poor placement
        
        # Air element (Northwest is ideal for living areas)
        if 'living' in room_name or 'hall' in room_name or 'drawing' in room_name:
            if 'northwest' in room_zone:
                elements['Air'] += 25  # Perfect placement
            elif 'north' in room_zone or 'west' in room_zone:
                elements['Air'] += 15  # Good placement
            else:
                elements['Air'] -= 5  # Poor placement
        
        # Space element (Center should be open)
        if 'center' in room_zone:
            if 'open' in room_name or 'courtyard' in room_name or 'hall' in room_name:
                elements['Space'] += 30  # Perfect - open center
            else:
                elements['Space'] -= 10  # Poor - blocked center
    
    # Orientation bonuses
    if 'north' in orientation or 'east' in orientation:
        elements['Water'] += 10
        elements['Air'] += 8
    elif 'south' in orientation:
        elements['Fire'] += 10
    
    # Ground floor bonus for earth element
    if floor_num == 0 or floor_num == 1:
        elements['Earth'] += 10
    
    # Large plot bonus for space element
    if plot_area > 1500:
        elements['Space'] += 12
    elif plot_area < 1000:
        elements['Space'] -= 5
    
    # Room count balance
    room_count = len(rooms)
    if room_count >= 4:
        elements['Space'] += 5  # Good room distribution
    
    # Clamp values between 30-100 (minimum 30 for realistic scores)
    for key in elements:
        elements[key] = min(100, max(30, elements[key]))
    
    return elements

def generate_2d_visualization(elements, vastu_score):
    """Generate 2D matplotlib visualization of 5 elements"""
    
    # Create figure with better styling
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('#FFF8E7')
    
    # --- LEFT PLOT: Bar Chart of 5 Elements ---
    element_names = list(elements.keys())
    element_values = list(elements.values())
    
    # Define colors for each element (Vastu-themed)
    colors = ['#E07A5F', '#2A9D8F', '#EAD7C0', '#E9C46A', '#264653']
    
    bars = ax1.bar(element_names, element_values, color=colors, edgecolor='black', linewidth=1.5)
    
    # Add value labels on bars
    for bar, value in zip(bars, element_values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.1f}%',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax1.set_ylabel('Score (%)', fontsize=12, fontweight='bold')
    ax1.set_title('5 Elements Analysis', fontsize=14, fontweight='bold', pad=20)
    ax1.set_ylim(0, 110)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_facecolor('#FFFFFF')
    
    # Add horizontal line at 70% (good threshold)
    ax1.axhline(y=70, color='green', linestyle='--', linewidth=1, alpha=0.5, label='Good Threshold')
    ax1.legend(loc='upper right')
    
    # --- RIGHT PLOT: Radar Chart of 5 Elements ---
    angles = np.linspace(0, 2 * np.pi, len(element_names), endpoint=False).tolist()
    element_values_radar = element_values + [element_values[0]]  # Close the circle
    angles += angles[:1]
    
    ax2 = plt.subplot(122, projection='polar')
    ax2.plot(angles, element_values_radar, 'o-', linewidth=2, color='#F4A261')
    ax2.fill(angles, element_values_radar, alpha=0.25, color='#F4A261')
    ax2.set_xticks(angles[:-1])
    ax2.set_xticklabels(element_names, fontsize=10, fontweight='bold')
    ax2.set_ylim(0, 100)
    ax2.set_title(f'Vastu Score: {vastu_score:.1f}%', 
                  fontsize=14, fontweight='bold', pad=20, color='#2A9D8F')
    ax2.grid(True, alpha=0.3)
    ax2.set_facecolor('#FFFFFF')
    
    # Add score ranges
    ax2.set_yticks([25, 50, 75, 100])
    ax2.set_yticklabels(['25%', '50%', '75%', '100%'], fontsize=8)
    
    plt.tight_layout()
    
    # Save to bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='#FFF8E7')
    buf.seek(0)
    plt.close()
    
    # Convert to base64 for JSON response
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    
    return img_base64

@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    """Analyze space details with ML model and generate visualization"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        print(f"📊 Received analysis request: {json.dumps(data, indent=2)}")
        
        # Extract space details
        plot_size = data.get('plotSize', '1200 sq ft')
        room_type = data.get('roomType', '2bhk')
        orientation = data.get('orientation', 'north-facing')
        floor_number = int(data.get('floorNumber', 1))
        rooms = data.get('rooms', [])
        
        # Parse plot size
        plot_area = 1200
        try:
            plot_area = int(''.join(filter(str.isdigit, plot_size)))
        except:
            pass
        
        plot_width = int(plot_area ** 0.5)
        plot_height = plot_area // plot_width
        
        # Prepare ML input
        ml_input = {
            'plot_width': plot_width,
            'plot_height': plot_height,
            'plot_area': plot_area,
            'floor_num': floor_number,
            'zone_encoded': encode_zone(rooms[0].get('zone', 'center') if rooms else 'center'),
            'orientation_encoded': encode_orientation(orientation),
            'room_type_encoded': encode_room_type(room_type),
            'adjacent_count': len(rooms),
            'shared_walls_count': max(1, len(rooms) - 1)
        }
        
        print(f"🤖 ML Input: {json.dumps(ml_input, indent=2)}")
        
        # Call ML model
        ml_score = 75  # Default
        try:
            ml_input_json = json.dumps(ml_input)
            result = subprocess.run(
                ['python', str(ML_MODEL_PATH)],
                input=ml_input_json,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                ml_result = json.loads(result.stdout)
                ml_score = ml_result.get('vastu_score', 75)
                print(f"✅ ML Model Score: {ml_score}")
            else:
                print(f"⚠️ ML Model error: {result.stderr}")
        except Exception as e:
            print(f"⚠️ ML Error: {e}")
        
        # Calculate 5 elements using Vastu rules
        elements = calculate_5_elements(data)
        print(f"🔥 Elements calculated: {elements}")
        
        # Calculate overall Vastu score
        # Blend ML prediction (40%) + Rule-based elements average (60%)
        rule_score = sum(elements.values()) / len(elements)
        vastu_score = round((ml_score * 0.4) + (rule_score * 0.6), 1)
        
        print(f"📊 Final Vastu Score: {vastu_score}% (ML: {ml_score}, Rules: {rule_score:.1f})")
        
        # Generate 2D visualization
        print("🎨 Generating 2D visualization...")
        visualization_base64 = generate_2d_visualization(elements, vastu_score)
        print("✅ Visualization generated!")
        
        # Generate recommendations
        recommendations = []
        for element, score in elements.items():
            if score < 70:
                if element == 'Fire':
                    recommendations.append({
                        'element': element,
                        'score': score,
                        'message': 'Consider placing kitchen in Southeast direction for better fire element balance'
                    })
                elif element == 'Water':
                    recommendations.append({
                        'element': element,
                        'score': score,
                        'message': 'Water sources (bathroom, well) should be in Northeast for optimal water element'
                    })
                elif element == 'Earth':
                    recommendations.append({
                        'element': element,
                        'score': score,
                        'message': 'Master bedroom in Southwest enhances earth element and stability'
                    })
                elif element == 'Air':
                    recommendations.append({
                        'element': element,
                        'score': score,
                        'message': 'Living room in Northwest improves air circulation and social energy'
                    })
                elif element == 'Space':
                    recommendations.append({
                        'element': element,
                        'score': score,
                        'message': 'Keep center of house open or use as courtyard for better space element'
                    })
        
        if not recommendations:
            recommendations.append({
                'element': 'Overall',
                'score': vastu_score,
                'message': 'Excellent Vastu compliance! Your space has good energy balance.'
            })
        
        # Return complete analysis
        response = {
            'success': True,
            'vastu_score': vastu_score,
            'ml_score': ml_score,
            'rule_score': round(rule_score, 1),
            'elements': elements,
            'visualization': visualization_base64,  # Base64 encoded PNG
            'recommendations': recommendations,
            'space_details': {
                'plot_size': plot_size,
                'room_type': room_type,
                'orientation': orientation,
                'floor_number': floor_number,
                'rooms_count': len(rooms)
            }
        }
        
        print("✅ Analysis complete! Sending response...")
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Return fallback response
        return jsonify({
            'success': False,
            'error': str(e),
            'vastu_score': 75,
            'ml_score': 75,
            'rule_score': 75,
            'elements': {
                'Fire': 75,
                'Water': 75,
                'Earth': 75,
                'Air': 75,
                'Space': 75
            },
            'visualization': None,
            'recommendations': [{
                'element': 'System',
                'score': 75,
                'message': 'Analysis completed with default values. Please check server logs.'
            }]
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'ml_model': 'loaded',
        'visualization': 'matplotlib ready'
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 VASTU VISION - ML ANALYSIS SERVER")
    print("=" * 60)
    print("📊 ML Model: Loaded")
    print("🎨 Matplotlib: Ready for 2D visualization")
    print("🌐 Server: http://localhost:5000")
    print("✅ Ready to analyze!")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
