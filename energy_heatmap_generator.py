#!/usr/bin/env python3
"""
Energy Balance Heatmap Generator
Creates visual heatmaps showing Vastu energy balance (Fire/Water/Air/Earth/Space zones)
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import io
import base64
import json
from typing import Dict, Any, List

app = Flask(__name__)
CORS(app)

# Vastu Energy Zone Mapping
ENERGY_ZONES = {
    'northeast': {'elements': ['water', 'space'], 'strength': 1.0, 'color': '#4A90E2'},
    'east': {'elements': ['air', 'water'], 'strength': 0.9, 'color': '#7ED321'},
    'southeast': {'elements': ['fire'], 'strength': 1.0, 'color': '#F5A623'},
    'south': {'elements': ['fire'], 'strength': 0.9, 'color': '#D0021B'},
    'southwest': {'elements': ['earth'], 'strength': 1.0, 'color': '#9013FE'},
    'west': {'elements': ['air', 'fire'], 'strength': 0.9, 'color': '#50E3C2'},
    'northwest': {'elements': ['air'], 'strength': 1.0, 'color': '#B8E986'},
    'north': {'elements': ['water', 'air'], 'strength': 0.9, 'color': '#417505'},
    'center': {'elements': ['space'], 'strength': 1.0, 'color': '#BD10E0'}
}

# Element Colors
ELEMENT_COLORS = {
    'fire': '#FF6B6B',
    'water': '#4ECDC4',
    'earth': '#95E1D3',
    'air': '#F38181',
    'space': '#AA96DA'
}

def calculate_zone_energy(space_data: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
    """Calculate energy levels for each zone using PROPER VASTU PRINCIPLES"""
    
    rooms = space_data.get('rooms', [])
    orientation = space_data.get('orientation', 'north-facing')
    plot_size = space_data.get('plotSize', '1200 sq ft')
    
    # Initialize zone energy map
    zone_energy = {}
    for zone in ENERGY_ZONES:
        zone_energy[zone] = {
            'fire': 0.0,
            'water': 0.0,
            'earth': 0.0,
            'air': 0.0,
            'space': 0.0
        }
    
    # VASTU COMPLIANCE MAPPING - Proper element to zone alignment
    # According to Vastu Shastra principles:
    vastu_optimal_placements = {
        'kitchen': {'zone': 'southeast', 'element': 'fire', 'score': 1.0},
        'southeast': {'element': 'fire', 'base_energy': 0.8},
        'bathroom': {'zone': 'northwest', 'element': 'water', 'score': 1.0},
        'toilet': {'zone': 'northwest', 'element': 'water', 'score': 1.0},
        'northwest': {'element': 'water', 'base_energy': 0.6},
        'bedroom': {'zone': 'southwest', 'element': 'earth', 'score': 1.0},
        'master bedroom': {'zone': 'southwest', 'element': 'earth', 'score': 1.0},
        'southwest': {'element': 'earth', 'base_energy': 0.8},
        'living room': {'zone': 'northeast', 'element': 'air', 'score': 0.9},
        'hall': {'zone': 'northeast', 'element': 'air', 'score': 0.9},
        'dining room': {'zone': 'west', 'element': 'air', 'score': 0.8},
        'study room': {'zone': 'northeast', 'element': 'air', 'score': 0.85},
        'puja room': {'zone': 'northeast', 'element': 'space', 'score': 1.0},
        'prayer room': {'zone': 'northeast', 'element': 'space', 'score': 1.0},
        'northeast': {'element': 'space', 'base_energy': 0.9},
        'store room': {'zone': 'southwest', 'element': 'earth', 'score': 0.8},
        'center': {'element': 'space', 'base_energy': 0.7}  # Brahmasthan should be open
    }
    
    # Calculate compliance score for each room placement
    for room in rooms:
        room_name = room.get('name', '').lower()
        room_zone = room.get('zone', '').lower()
        
        if room_zone not in zone_energy:
            continue
        
        # Find optimal placement for this room type
        optimal_zone = None
        room_element = None
        compliance_score = 0.5  # Default low score
        
        for room_type, placement_info in vastu_optimal_placements.items():
            if room_type in room_name or (room_type == room_zone):
                optimal_zone = placement_info.get('zone', room_zone)
                room_element = placement_info.get('element')
                compliance_score = placement_info.get('score', 0.5)
                break
        
        # If room type not found, try to determine from name
        if not room_element:
            if 'kitchen' in room_name or 'cook' in room_name:
                room_element = 'fire'
                optimal_zone = 'southeast'
                compliance_score = 1.0 if room_zone == 'southeast' else 0.3
            elif 'bath' in room_name or 'toilet' in room_name or 'wc' in room_name:
                room_element = 'water'
                optimal_zone = 'northwest'
                compliance_score = 1.0 if room_zone == 'northwest' else 0.3
            elif 'bed' in room_name or 'master' in room_name:
                room_element = 'earth'
                optimal_zone = 'southwest'
                compliance_score = 1.0 if room_zone == 'southwest' else 0.3
            elif 'living' in room_name or 'hall' in room_name or 'drawing' in room_name:
                room_element = 'air'
                optimal_zone = 'northeast'
                compliance_score = 0.9 if room_zone == 'northeast' else 0.4
            elif 'puja' in room_name or 'prayer' in room_name or 'temple' in room_name:
                room_element = 'space'
                optimal_zone = 'northeast'
                compliance_score = 1.0 if room_zone == 'northeast' else 0.2
            else:
                room_element = 'air'  # Default
                compliance_score = 0.5
        
        # Calculate energy contribution based on compliance
        if room_element:
            # Primary element energy (based on compliance)
            zone_energy[room_zone][room_element] += compliance_score
            
            # Add zone's natural element affinity
            zone_info = ENERGY_ZONES.get(room_zone, {})
            for zone_element in zone_info.get('elements', []):
                if zone_element != room_element:
                    zone_energy[room_zone][zone_element] += 0.2 * compliance_score
            
            # Penalty for wrong placement (subtract from optimal zone)
            if optimal_zone and optimal_zone != room_zone:
                # Wrong placement reduces energy
                zone_energy[optimal_zone][room_element] += 0.1  # Minimal positive
                zone_energy[room_zone][room_element] *= 0.7  # Reduce energy for wrong placement
    
    # Add orientation-based energy (proper Vastu orientation benefits)
    orientation_benefits = {
        'north-facing': {'north': 0.3, 'northeast': 0.4, 'northwest': 0.2},
        'northeast-facing': {'northeast': 0.5, 'north': 0.3, 'east': 0.3},
        'east-facing': {'east': 0.4, 'northeast': 0.3, 'southeast': 0.2},
        'southeast-facing': {'southeast': 0.4, 'east': 0.3},
        'south-facing': {'south': 0.3, 'southeast': 0.3, 'southwest': 0.2},
        'southwest-facing': {'southwest': 0.4, 'south': 0.3},
        'west-facing': {'west': 0.3, 'northwest': 0.3, 'southwest': 0.2},
        'northwest-facing': {'northwest': 0.4, 'north': 0.2, 'west': 0.2}
    }
    
    orient_key = orientation.lower().replace(' ', '-')
    if orient_key in orientation_benefits:
        for zone, energy_boost in orientation_benefits[orient_key].items():
            if zone in zone_energy:
                # Boost the zone's natural elements
                zone_info = ENERGY_ZONES.get(zone, {})
                for elem in zone_info.get('elements', []):
                    zone_energy[zone][elem] += energy_boost
    
    # Check center (Brahmasthan) - should be mostly empty
    has_center_room = any('center' in r.get('zone', '').lower() for r in rooms)
    if has_center_room:
        zone_energy['center']['space'] *= 0.5  # Penalty for center obstruction
    
    # Normalize and scale energy levels (0-1 scale)
    max_energy = 0
    for zone in zone_energy:
        for element in zone_energy[zone]:
            max_energy = max(max_energy, zone_energy[zone][element])
    
    if max_energy > 0:
        for zone in zone_energy:
            for element in zone_energy[zone]:
                zone_energy[zone][element] = min(1.0, zone_energy[zone][element] / max_energy)
    
    return zone_energy

def generate_energy_heatmap(space_data: Dict[str, Any], element: str = 'all') -> str:
    """Generate energy balance heatmap visualization"""
    
    zone_energy = calculate_zone_energy(space_data)
    rooms = space_data.get('rooms', [])
    
    # Create figure with 3x3 grid representing Vastu zones
    fig, axes = plt.subplots(1, 1, figsize=(12, 12))
    ax = axes
    
    # Create 3x3 grid
    grid_size = 3
    zone_positions = {
        'northwest': (0, 0), 'north': (0, 1), 'northeast': (0, 2),
        'west': (1, 0), 'center': (1, 1), 'east': (1, 2),
        'southwest': (2, 0), 'south': (2, 1), 'southeast': (2, 2)
    }
    
    # Create heatmap matrix
    if element == 'all':
        # Composite heatmap showing dominant element per zone
        heatmap_data = np.zeros((grid_size, grid_size))
        element_map = np.zeros((grid_size, grid_size), dtype=int)
        
        for zone, pos in zone_positions.items():
            energies = zone_energy[zone]
            dominant_element = max(energies.items(), key=lambda x: x[1])
            heatmap_data[pos] = dominant_element[1]
            
            # Map element to number for color
            element_to_num = {'fire': 0, 'water': 1, 'earth': 2, 'air': 3, 'space': 4}
            element_map[pos] = element_to_num.get(dominant_element[0], 0)
        
        # Create custom colormap for each element
        colors_list = [
            ELEMENT_COLORS['fire'],
            ELEMENT_COLORS['water'],
            ELEMENT_COLORS['earth'],
            ELEMENT_COLORS['air'],
            ELEMENT_COLORS['space']
        ]
        
        # Create heatmap
        im = ax.imshow(element_map, cmap=mcolors.ListedColormap(colors_list), 
                      vmin=0, vmax=4, alpha=0.7, interpolation='nearest')
        
        # Overlay energy intensity
        for zone, pos in zone_positions.items():
            energies = zone_energy[zone]
            max_energy = max(energies.values())
            if max_energy > 0:
                # Add intensity overlay
                rect = plt.Rectangle((pos[1]-0.5, pos[0]-0.5), 1, 1,
                                   fill=True, alpha=max_energy*0.5, 
                                   color='white', edgecolor='black', linewidth=2)
                ax.add_patch(rect)
                
                # Add text labels
                zone_label = zone.replace('north', 'N').replace('south', 'S').replace('east', 'E').replace('west', 'W')
                ax.text(pos[1], pos[0], f'{zone_label}\n{max_energy:.0%}', 
                       ha='center', va='center', fontsize=10, fontweight='bold')
    else:
        # Single element heatmap
        heatmap_data = np.zeros((grid_size, grid_size))
        
        for zone, pos in zone_positions.items():
            heatmap_data[pos] = zone_energy[zone].get(element, 0.0)
        
        im = ax.imshow(heatmap_data, cmap='viridis', vmin=0, vmax=1, 
                      interpolation='nearest', alpha=0.8)
        
        # Add zone labels
        for zone, pos in zone_positions.items():
            energy_val = zone_energy[zone].get(element, 0.0)
            zone_label = zone.replace('north', 'N').replace('south', 'S').replace('east', 'E').replace('west', 'W')
            ax.text(pos[1], pos[0], f'{zone_label}\n{energy_val:.0%}', 
                   ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    
    # Add room labels
    for room in rooms:
        room_zone = room.get('zone', '').lower()
        if room_zone in zone_positions:
            pos = zone_positions[room_zone]
            room_name = room.get('name', '')
            # Add small room label
            ax.text(pos[1], pos[0] + 0.25, room_name[:10], 
                   ha='center', va='top', fontsize=8, 
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    # Set axis labels
    ax.set_xticks(np.arange(grid_size))
    ax.set_yticks(np.arange(grid_size))
    ax.set_xticklabels(['West', 'Center', 'East'])
    ax.set_yticklabels(['North', 'Center', 'South'])
    ax.set_xlabel('Direction →', fontsize=12, fontweight='bold')
    ax.set_ylabel('Direction ↑', fontsize=12, fontweight='bold')
    
    # Add title
    title = f'Vastu Energy Balance Heatmap - {"All Elements" if element == "all" else element.capitalize()}'
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    # Add colorbar if single element
    if element != 'all':
        plt.colorbar(im, ax=ax, label=f'{element.capitalize()} Energy Level')
    else:
        # Add legend for all elements
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=ELEMENT_COLORS['fire'], label='Fire'),
            Patch(facecolor=ELEMENT_COLORS['water'], label='Water'),
            Patch(facecolor=ELEMENT_COLORS['earth'], label='Earth'),
            Patch(facecolor=ELEMENT_COLORS['air'], label='Air'),
            Patch(facecolor=ELEMENT_COLORS['space'], label='Space')
        ]
        ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.05, 1))
    
    plt.tight_layout()
    
    # Convert to base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    plt.close()
    
    return base64.b64encode(buf.read()).decode('utf-8')

@app.route('/generate_heatmap', methods=['POST', 'OPTIONS'])
def generate_heatmap():
    """Generate energy balance heatmap"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        element = data.get('element', 'all')
        
        print(f"🔥 Generating energy heatmap for element: {element}")
        
        heatmap_image = generate_energy_heatmap(data, element)
        
        # Get zone energy data
        zone_energy = calculate_zone_energy(data)
        
        return jsonify({
            'success': True,
            'heatmap': heatmap_image,
            'zone_energy': zone_energy,
            'element': element
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/calculate_energy', methods=['POST', 'OPTIONS'])
def calculate_energy():
    """Calculate energy levels without generating image"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        zone_energy = calculate_zone_energy(data)
        
        # Calculate overall element balance
        element_balance = {
            'fire': 0.0,
            'water': 0.0,
            'earth': 0.0,
            'air': 0.0,
            'space': 0.0
        }
        
        for zone in zone_energy:
            for element, value in zone_energy[zone].items():
                element_balance[element] += value
        
        # Normalize
        total = sum(element_balance.values())
        if total > 0:
            for element in element_balance:
                element_balance[element] = element_balance[element] / total
        
        return jsonify({
            'success': True,
            'zone_energy': zone_energy,
            'element_balance': element_balance
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'service': 'energy_heatmap_generator'
    })

if __name__ == '__main__':
    print("=" * 70)
    print("🔥 VASTU VISION - ENERGY HEATMAP GENERATOR")
    print("=" * 70)
    print("✅ Fire/Water/Earth/Air/Space visualization")
    print("✅ Zone-based energy mapping")
    print("🌐 Server: http://localhost:5005")
    print("=" * 70)
    app.run(host='0.0.0.0', port=5005, debug=True)

