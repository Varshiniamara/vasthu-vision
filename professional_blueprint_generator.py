#!/usr/bin/env python3
"""
Professional Architectural Blueprint Generator
Creates highly detailed 2D floor plans with dimensions, furniture, doors, windows
Matches professional blueprints
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Arc, FancyBboxPatch
import numpy as np
import io
import base64
import json
from typing import Dict, Any, List, Tuple

app = Flask(__name__)
CORS(app)

# Vastu Zone to Position Mapping (relative to plot)
VASTU_ZONE_POSITIONS = {
    'northeast': (0.8, 0.8, 0.2, 0.2),  # (x, y, width, height) as fraction
    'north': (0.5, 0.8, 0.3, 0.2),
    'northwest': (0.0, 0.8, 0.2, 0.2),
    'east': (0.8, 0.5, 0.2, 0.3),
    'center': (0.35, 0.35, 0.3, 0.3),
    'west': (0.0, 0.5, 0.2, 0.3),
    'southeast': (0.8, 0.0, 0.2, 0.2),
    'south': (0.5, 0.0, 0.3, 0.2),
    'southwest': (0.0, 0.0, 0.2, 0.2)
}

def inches_to_feet(inches):
    """Convert inches to feet-inches format"""
    ft = int(inches // 12)
    inch = int(inches % 12)
    if inch == 0:
        return f"{ft}'"
    return f"{ft}'{inch}\""

def draw_professional_window(ax, x, y, width, height, position='top'):
    """Draw a professional window representation"""
    if position == 'top':
        # Window on top wall
        window_length = min(width * 0.4, 4)
        window_x = x + (width - window_length) / 2
        window_y = y + height
        # Outer frame
        ax.plot([window_x, window_x + window_length], [window_y, window_y], 
               'b-', linewidth=3)
        # Glass panes
        pane_count = 2
        for i in range(pane_count + 1):
            pane_x = window_x + (window_length / pane_count) * i
            ax.plot([pane_x, pane_x], [window_y - 0.1, window_y + 0.1], 
                   'b-', linewidth=1)
    elif position == 'bottom':
        window_length = min(width * 0.4, 4)
        window_x = x + (width - window_length) / 2
        window_y = y
        ax.plot([window_x, window_x + window_length], [window_y, window_y], 
               'b-', linewidth=3)
        for i in range(3):
            pane_x = window_x + (window_length / 2) * i
            ax.plot([pane_x, pane_x], [window_y - 0.1, window_y + 0.1], 
                   'b-', linewidth=1)
    elif position == 'left':
        window_length = min(height * 0.4, 4)
        window_x = x
        window_y = y + (height - window_length) / 2
        ax.plot([window_x, window_x], [window_y, window_y + window_length], 
               'b-', linewidth=3)
        for i in range(3):
            pane_y = window_y + (window_length / 2) * i
            ax.plot([window_x - 0.1, window_x + 0.1], [pane_y, pane_y], 
                   'b-', linewidth=1)
    elif position == 'right':
        window_length = min(height * 0.4, 4)
        window_x = x + width
        window_y = y + (height - window_length) / 2
        ax.plot([window_x, window_x], [window_y, window_y + window_length], 
               'b-', linewidth=3)
        for i in range(3):
            pane_y = window_y + (window_length / 2) * i
            ax.plot([window_x - 0.1, window_x + 0.1], [pane_y, pane_y], 
                   'b-', linewidth=1)

def draw_professional_door(ax, x, y, width, height, direction='right', swing='inward'):
    """Draw professional door with swing arc"""
    door_width = 3  # Standard door width in feet
    door_thickness = 0.3
    
    if direction == 'right':
        door_x = x + width - door_width
        door_y = y + height * 0.3
        # Door rectangle
        door_rect = patches.Rectangle((door_x, door_y), door_width, door_thickness,
                                      linewidth=2, edgecolor='black', facecolor='#8B4513')
        ax.add_patch(door_rect)
        # Swing arc
        arc = Arc((door_x, door_y + door_thickness), door_width*2, door_width*2,
                 angle=0, theta1=0, theta2=90, linewidth=2, color='black', linestyle='--')
        ax.add_patch(arc)
        # Door knob
        knob_x = door_x + door_width - 0.5
        knob_y = door_y + door_thickness/2
        knob = plt.Circle((knob_x, knob_y), 0.15, color='gold', zorder=10)
        ax.add_patch(knob)
    elif direction == 'top':
        door_x = x + width * 0.4
        door_y = y + height - door_thickness
        door_rect = patches.Rectangle((door_x, door_y), door_thickness, door_width,
                                      linewidth=2, edgecolor='black', facecolor='#8B4513')
        ax.add_patch(door_rect)
        arc = Arc((door_x + door_thickness, door_y), door_width*2, door_width*2,
                 angle=0, theta1=270, theta2=360, linewidth=2, color='black', linestyle='--')
        ax.add_patch(arc)
    elif direction == 'left':
        door_x = x
        door_y = y + height * 0.3
        door_rect = patches.Rectangle((door_x, door_y), door_width, door_thickness,
                                      linewidth=2, edgecolor='black', facecolor='#8B4513')
        ax.add_patch(door_rect)
        arc = Arc((door_x + door_width, door_y + door_thickness), door_width*2, door_width*2,
                 angle=0, theta1=90, theta2=180, linewidth=2, color='black', linestyle='--')
        ax.add_patch(arc)

def draw_detailed_bedroom(ax, x, y, width, height, room_name):
    """Draw detailed bedroom with bed, wardrobe, side table"""
    # Bed (typically 6' x 6'6" or 7')
    bed_width = min(7, width * 0.6)
    bed_height = min(6.5, height * 0.5)
    bed_x = x + width * 0.2
    bed_y = y + height * 0.3
    
    # Bed frame
    bed = patches.Rectangle((bed_x, bed_y), bed_width, bed_height,
                           linewidth=2, edgecolor='#654321', facecolor='#DEB887')
    ax.add_patch(bed)
    
    # Mattress
    mattress = patches.Rectangle((bed_x + 0.2, bed_y + 0.2), bed_width - 0.4, bed_height - 0.4,
                                linewidth=1, edgecolor='#8B4513', facecolor='#F5DEB3')
    ax.add_patch(mattress)
    
    # Pillows
    pillow_w = 1.5
    pillow_h = 1
    pillow1 = patches.Rectangle((bed_x + 0.5, bed_y + bed_height - 1.5), pillow_w, pillow_h,
                                linewidth=1, edgecolor='#333', facecolor='white')
    ax.add_patch(pillow1)
    pillow2 = patches.Rectangle((bed_x + bed_width - 2, bed_y + bed_height - 1.5), pillow_w, pillow_h,
                               linewidth=1, edgecolor='#333', facecolor='white')
    ax.add_patch(pillow2)
    
    # Wardrobe (along wall)
    wardrobe_w = min(6, width * 0.4)
    wardrobe_h = 2
    wardrobe_x = x + width - wardrobe_w - 1
    wardrobe_y = y + height * 0.1
    wardrobe = patches.Rectangle((wardrobe_x, wardrobe_y), wardrobe_w, wardrobe_h,
                                linewidth=2, edgecolor='#654321', facecolor='#D2691E')
    ax.add_patch(wardrobe)
    # Wardrobe door line
    ax.plot([wardrobe_x + wardrobe_w/2, wardrobe_x + wardrobe_w/2], 
           [wardrobe_y, wardrobe_y + wardrobe_h], 'k-', linewidth=1)
    
    # Side table
    table_size = 1.5
    table_x = bed_x + bed_width + 1
    table_y = bed_y + bed_height * 0.3
    table = patches.Rectangle((table_x, table_y), table_size, table_size,
                             linewidth=1, edgecolor='#333', facecolor='#DEB887')
    ax.add_patch(table)
    
    # TV stand (optional)
    if width > 12:
        tv_w = 4
        tv_h = 1
        tv_x = bed_x
        tv_y = bed_y - 2
        tv_stand = patches.Rectangle((tv_x, tv_y), tv_w, tv_h,
                                    linewidth=1, edgecolor='#333', facecolor='#696969')
        ax.add_patch(tv_stand)
        # TV screen
        tv_screen = patches.Rectangle((tv_x + 0.2, tv_y + 0.1), tv_w - 0.4, tv_h - 0.2,
                                     linewidth=1, edgecolor='#000', facecolor='#1C1C1C')
        ax.add_patch(tv_screen)

def draw_detailed_kitchen(ax, x, y, width, height):
    """Draw detailed kitchen with counter, stove, sink, refrigerator"""
    # Kitchen counter (L-shaped)
    counter_width = min(8, width * 0.7)
    counter_height = min(2.5, height * 0.6)
    counter_x = x + width * 0.15
    counter_y = y + height * 0.2
    
    # Main counter
    counter = patches.Rectangle((counter_x, counter_y), counter_width, counter_height,
                               linewidth=2, edgecolor='#333', facecolor='#D3D3D3')
    ax.add_patch(counter)
    
    # L-shaped extension
    if width > 10:
        counter_ext_w = 3
        counter_ext_h = counter_height
        counter_ext = patches.Rectangle((counter_x, counter_y - counter_ext_h), 
                                       counter_ext_w, counter_ext_h,
                                       linewidth=2, edgecolor='#333', facecolor='#D3D3D3')
        ax.add_patch(counter_ext)
    
    # Stove (4 burner)
    stove_size = 2.5
    stove_x = counter_x + counter_width * 0.3
    stove_y = counter_y + counter_height * 0.2
    stove = patches.Rectangle((stove_x, stove_y), stove_size, stove_size,
                             linewidth=2, edgecolor='#000', facecolor='#2F2F2F')
    ax.add_patch(stove)
    # Burners
    for i in range(2):
        for j in range(2):
            burner_x = stove_x + stove_size/4 + (stove_size/2) * i
            burner_y = stove_y + stove_size/4 + (stove_size/2) * j
            burner = plt.Circle((burner_x, burner_y), 0.3, color='red', zorder=5)
            ax.add_patch(burner)
    
    # Sink
    sink_size = 2
    sink_x = counter_x + counter_width * 0.7
    sink_y = counter_y + counter_height * 0.3
    sink = patches.Rectangle((sink_x, sink_y), sink_size, sink_size,
                            linewidth=2, edgecolor='#4169E1', facecolor='#B0E0E6')
    ax.add_patch(sink)
    # Faucet
    ax.plot([sink_x + sink_size/2, sink_x + sink_size/2], 
           [sink_y + sink_size, sink_y + sink_size + 0.5], 'k-', linewidth=2)
    
    # Refrigerator
    fridge_w = 2.5
    fridge_h = min(6, height * 0.8)
    fridge_x = x + width - fridge_w - 1
    fridge_y = y + height * 0.1
    fridge = patches.Rectangle((fridge_x, fridge_y), fridge_w, fridge_h,
                              linewidth=2, edgecolor='#000', facecolor='#E0E0E0')
    ax.add_patch(fridge)
    # Fridge door line
    ax.plot([fridge_x + fridge_w/2, fridge_x + fridge_w/2], 
           [fridge_y, fridge_y + fridge_h], 'k-', linewidth=2)

def draw_detailed_living_room(ax, x, y, width, height):
    """Draw detailed living room with sofa set, coffee table"""
    center_x = x + width / 2
    center_y = y + height / 2
    
    # Main sofa (facing center)
    sofa_length = min(8, width * 0.6)
    sofa_width = 3
    sofa_x = center_x - sofa_length/2
    sofa_y = y + height * 0.3
    sofa = patches.Rectangle((sofa_x, sofa_y), sofa_length, sofa_width,
                            linewidth=2, edgecolor='#654321', facecolor='#8B4513')
    ax.add_patch(sofa)
    # Sofa cushions
    cushion_count = 3
    for i in range(cushion_count):
        cushion_x = sofa_x + (sofa_length / cushion_count) * i
        ax.plot([cushion_x, cushion_x], [sofa_y, sofa_y + sofa_width], 
               'k-', linewidth=1)
    
    # Coffee table
    table_size = min(4, width * 0.3)
    table = plt.Circle((center_x, center_y), table_size/2,
                      linewidth=2, edgecolor='#654321', facecolor='#DEB887')
    ax.add_patch(table)
    
    # Armchairs
    chair_size = 2.5
    chair1 = patches.Rectangle((center_x - chair_size*1.5, sofa_y + sofa_width + 2), 
                               chair_size, chair_size,
                               linewidth=1, edgecolor='#654321', facecolor='#8B4513')
    ax.add_patch(chair1)
    chair2 = patches.Rectangle((center_x + chair_size*0.5, sofa_y + sofa_width + 2), 
                               chair_size, chair_size,
                               linewidth=1, edgecolor='#654321', facecolor='#8B4513')
    ax.add_patch(chair2)
    
    # TV stand
    tv_w = min(6, width * 0.4)
    tv_h = 1.5
    tv_x = center_x - tv_w/2
    tv_y = y + height * 0.1
    tv_stand = patches.Rectangle((tv_x, tv_y), tv_w, tv_h,
                               linewidth=1, edgecolor='#333', facecolor='#696969')
    ax.add_patch(tv_stand)
    # TV screen
    tv_screen = patches.Rectangle((tv_x + 0.2, tv_y + 0.1), tv_w - 0.4, tv_h - 0.2,
                                 linewidth=1, edgecolor='#000', facecolor='#1C1C1C')
    ax.add_patch(tv_screen)

def draw_detailed_dining_room(ax, x, y, width, height):
    """Draw detailed dining room with table and chairs"""
    center_x = x + width / 2
    center_y = y + height / 2
    
    # Dining table (rectangular or round)
    table_length = min(6, width * 0.7)
    table_width = min(3, height * 0.6)
    table_x = center_x - table_length/2
    table_y = center_y - table_width/2
    table = patches.Rectangle((table_x, table_y), table_length, table_width,
                             linewidth=2, edgecolor='#654321', facecolor='#DEB887')
    ax.add_patch(table)
    
    # Chairs (6 chairs around table)
    chair_w = 1.5
    chair_h = 1.5
    chair_positions = [
        (center_x - table_length/2 - chair_w - 0.3, center_y),  # Left
        (center_x + table_length/2 + 0.3, center_y),  # Right
        (center_x, center_y - table_width/2 - chair_h - 0.3),  # Bottom
        (center_x, center_y + table_width/2 + 0.3),  # Top
        (center_x - table_length/3, center_y - table_width/2 - chair_h - 0.3),  # Bottom-left
        (center_x + table_length/3, center_y - table_width/2 - chair_h - 0.3),  # Bottom-right
    ]
    
    for chair_x, chair_y in chair_positions[:6]:  # Limit to 6 chairs
        if chair_x + chair_w < x + width and chair_y + chair_h < y + height:
            chair = patches.Rectangle((chair_x, chair_y), chair_w, chair_h,
                                     linewidth=1, edgecolor='#654321', facecolor='#8B4513')
            ax.add_patch(chair)

def draw_detailed_bathroom(ax, x, y, width, height):
    """Draw detailed bathroom with toilet, sink, shower"""
    # Toilet
    toilet_w = 1.5
    toilet_h = 2
    toilet_x = x + width * 0.2
    toilet_y = y + height * 0.3
    toilet = patches.Rectangle((toilet_x, toilet_y), toilet_w, toilet_h,
                             linewidth=1, edgecolor='#333', facecolor='white')
    ax.add_patch(toilet)
    # Toilet seat
    seat = patches.Rectangle((toilet_x + 0.1, toilet_y + toilet_h - 0.3), 
                            toilet_w - 0.2, 0.3,
                            linewidth=1, edgecolor='#000', facecolor='#E0E0E0')
    ax.add_patch(seat)
    
    # Sink
    sink_size = 1.5
    sink_x = x + width - sink_size - 1
    sink_y = y + height * 0.6
    sink = patches.Rectangle((sink_x, sink_y), sink_size, sink_size,
                            linewidth=1, edgecolor='#4169E1', facecolor='#B0E0E6')
    ax.add_patch(sink)
    # Faucet
    ax.plot([sink_x + sink_size/2, sink_x + sink_size/2], 
           [sink_y + sink_size, sink_y + sink_size + 0.3], 'k-', linewidth=1)
    
    # Shower (if space permits)
    if width > 5 and height > 5:
        shower_size = 3
        shower_x = x + width * 0.5
        shower_y = y + height * 0.2
        shower = patches.Rectangle((shower_x, shower_y), shower_size, shower_size,
                                  linewidth=2, edgecolor='#4169E1', facecolor='#E0F6FF')
        ax.add_patch(shower)

def generate_professional_blueprint(space_data: Dict[str, Any]) -> str:
    """Generate a highly detailed professional blueprint"""
    
    plot_size = space_data.get('plotSize', '1200 sq ft')
    rooms = space_data.get('rooms', [])
    orientation = space_data.get('orientation', 'north-facing')
    room_type = space_data.get('roomType', '2bhk')
    
    # Calculate plot dimensions
    try:
        plot_area = int(''.join(filter(str.isdigit, plot_size)))
    except:
        plot_area = 1200
    
    # Calculate reasonable plot dimensions
    if plot_area <= 1200:
        plot_width, plot_height = 30, 40  # 30x40 ft
    elif plot_area <= 2000:
        plot_width, plot_height = 35, 50  # 35x50 ft
    elif plot_area <= 2800:
        plot_width, plot_height = 40, 60  # 40x60 ft
    else:
        plot_width, plot_height = 50, 70  # 50x70 ft
    
    # Create figure
    fig, ax = plt.subplots(figsize=(20, 24))
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FFFFFF')
    
    margin = 5
    ax.set_xlim(-margin, plot_width + margin)
    ax.set_ylim(-margin, plot_height + margin)
    ax.set_aspect('equal')
    
    # Draw outer walls (thick black lines)
    outer_wall = patches.Rectangle((0, 0), plot_width, plot_height,
                                   linewidth=10, edgecolor='#000000', facecolor='none')
    ax.add_patch(outer_wall)
    
    # Process user-defined rooms and create layout
    room_placements = {}
    for room in rooms:
        room_name = room.get('name', '').lower()
        room_zone = room.get('zone', '').lower()
        
        if room_zone in VASTU_ZONE_POSITIONS:
            zone_pos = VASTU_ZONE_POSITIONS[room_zone]
            room_width = plot_width * zone_pos[2]
            room_height = plot_height * zone_pos[3]
            room_x = plot_width * zone_pos[0]
            room_y = plot_height * zone_pos[1]
            
            # Ensure rooms fit properly
            room_width = min(room_width, plot_width * 0.4)
            room_height = min(room_height, plot_height * 0.4)
            
            room_placements[room_name] = {
                'x': room_x, 'y': room_y, 'width': room_width, 'height': room_height,
                'zone': room_zone, 'name': room.get('name', 'Room')
            }
    
    # Add default rooms if user didn't specify enough
    default_rooms = {
        'kitchen': {'zone': 'southeast', 'type': 'kitchen'},
        'bedroom': {'zone': 'southwest', 'type': 'bedroom'},
        'living room': {'zone': 'northeast', 'type': 'living'},
        'bathroom': {'zone': 'northwest', 'type': 'bathroom'},
        'dining room': {'zone': 'west', 'type': 'dining'}
    }
    
    for room_key, room_info in default_rooms.items():
        if room_key not in room_placements:
            zone_pos = VASTU_ZONE_POSITIONS[room_info['zone']]
            room_width = plot_width * zone_pos[2]
            room_height = plot_height * zone_pos[3]
            room_x = plot_width * zone_pos[0]
            room_y = plot_height * zone_pos[1]
            
            room_width = min(room_width, plot_width * 0.35)
            room_height = min(room_height, plot_height * 0.35)
            
            room_placements[room_key] = {
                'x': room_x, 'y': room_y, 'width': room_width, 'height': room_height,
                'zone': room_info['zone'], 'name': room_key.title(), 'type': room_info['type']
            }
    
    # Draw all rooms
    for room_name, room_data in room_placements.items():
        x, y = room_data['x'], room_data['y']
        width, height = room_data['width'], room_data['height']
        
        # Interior walls
        wall = patches.Rectangle((x, y), width, height,
                                linewidth=5, edgecolor='#000000', facecolor='#F5F5F5')
        ax.add_patch(wall)
        
        # Room dimensions (in feet and inches)
        dim_text = f"{int(width)}'{int((width % 1) * 12)}\" × {int(height)}'{int((height % 1) * 12)}\""
        
        # Room label
        center_x = x + width / 2
        center_y = y + height / 2
        
        # Background for label
        label_bg = patches.Rectangle((center_x - width*0.4, center_y + height*0.35), 
                                    width*0.8, height*0.15,
                                    linewidth=2, edgecolor='#000', facecolor='white', alpha=0.95)
        ax.add_patch(label_bg)
        
        ax.text(center_x, center_y + height*0.42, room_data['name'].upper(),
               ha='center', va='center', fontsize=14, fontweight='bold', color='#000')
        
        # Dimensions below label
        ax.text(center_x, center_y - height*0.35, dim_text,
               ha='center', va='center', fontsize=11, style='italic', 
               color='#555', fontweight='600',
               bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF8DC', edgecolor='#666', alpha=0.9))
        
        # Draw detailed furniture based on room type
        room_type = room_data.get('type', 'bedroom')
        if 'bedroom' in room_type.lower() or 'bed' in room_name:
            draw_detailed_bedroom(ax, x, y, width, height, room_data['name'])
        elif 'kitchen' in room_type.lower() or 'kitchen' in room_name:
            draw_detailed_kitchen(ax, x, y, width, height)
        elif 'living' in room_type.lower() or 'living' in room_name or 'drawing' in room_name:
            draw_detailed_living_room(ax, x, y, width, height)
        elif 'dining' in room_type.lower() or 'dining' in room_name:
            draw_detailed_dining_room(ax, x, y, width, height)
        elif 'bath' in room_type.lower() or 'toilet' in room_type.lower():
            draw_detailed_bathroom(ax, x, y, width, height)
        
        # Windows (on exterior walls)
        if x == 0:  # Left wall
            draw_professional_window(ax, x, y, width, height, 'left')
        if x + width == plot_width:  # Right wall
            draw_professional_window(ax, x, y, width, height, 'right')
        if y == 0:  # Bottom wall
            draw_professional_window(ax, x, y, width, height, 'bottom')
        if y + height == plot_height:  # Top wall
            draw_professional_window(ax, x, y, width, height, 'top')
        
        # Doors (one per room on interior walls)
        if x > 0:  # Has left wall
            draw_professional_door(ax, x, y, width, height, 'left')
        elif y > 0:  # Has bottom wall
            draw_professional_door(ax, x, y, width, height, 'top')
    
    # Main entrance door (based on orientation)
    entrance_width = 4
    entrance_thickness = 0.5
    if 'north' in orientation.lower():
        entrance_x = plot_width * 0.6
        entrance_y = plot_height - entrance_thickness
        entrance = patches.Rectangle((entrance_x, entrance_y), entrance_width, entrance_thickness,
                                    linewidth=3, edgecolor='#000', facecolor='#8B4513')
        ax.add_patch(entrance)
        ax.text(entrance_x + entrance_width/2, entrance_y - 0.8, 'MAIN DOOR',
               ha='center', fontsize=10, fontweight='bold')
    
    # Professional compass
    compass_x = plot_width + margin * 0.3
    compass_y = plot_height + margin * 0.3
    compass_size = 4
    
    # Compass circle
    compass_circle = plt.Circle((compass_x, compass_y), compass_size,
                               fill=False, edgecolor='red', linewidth=3)
    ax.add_patch(compass_circle)
    
    # North arrow (bold red)
    ax.arrow(compass_x, compass_y, 0, compass_size*0.8,
            head_width=1, head_length=0.8, fc='red', ec='red', linewidth=4)
    ax.text(compass_x, compass_y + compass_size*0.8 + 1.2, 'N',
           ha='center', fontsize=18, fontweight='bold', color='red')
    
    # Other directions
    ax.text(compass_x + compass_size*0.7, compass_y, 'E',
           ha='center', fontsize=14, fontweight='bold', color='#000')
    ax.text(compass_x, compass_y - compass_size*0.7, 'S',
           ha='center', fontsize=14, fontweight='bold', color='#000')
    ax.text(compass_x - compass_size*0.7, compass_y, 'W',
           ha='center', fontsize=14, fontweight='bold', color='#000')
    
    # Title
    title_text = f"{room_type.upper()} FLOOR PLAN - {orientation.upper().replace('-', ' ')}"
    title_y = plot_height + margin * 0.6
    ax.text(plot_width/2, title_y, title_text,
           ha='center', fontsize=22, fontweight='bold', color='#000',
           bbox=dict(boxstyle='round,pad=1', facecolor='#F4A261', edgecolor='#000', linewidth=3))
    
    # Overall dimensions
    dim_text = f"Overall: {plot_width}' × {plot_height}' (Approx. {plot_area} sq ft)"
    ax.text(plot_width/2, -margin*0.8, dim_text,
           ha='center', fontsize=12, fontweight='bold', style='italic', color='#555')
    
    # Scale bar
    scale_length = 10
    scale_x = 5
    scale_y = -margin * 0.5
    ax.plot([scale_x, scale_x + scale_length], [scale_y, scale_y], 'k-', linewidth=4)
    ax.plot([scale_x, scale_x], [scale_y - 0.5, scale_y + 0.5], 'k-', linewidth=4)
    ax.plot([scale_x + scale_length, scale_x + scale_length], [scale_y - 0.5, scale_y + 0.5], 'k-', linewidth=4)
    ax.text(scale_x + scale_length/2, scale_y - 1.5, f"SCALE: {scale_length} FEET",
           ha='center', fontsize=11, fontweight='bold', style='italic')
    
    # Remove axes
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    plt.tight_layout()
    
    # Save
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight', facecolor='#FAFAFA')
    buf.seek(0)
    plt.close()
    
    return base64.b64encode(buf.read()).decode('utf-8')

@app.route('/generate_professional_blueprint', methods=['POST', 'OPTIONS'])
def generate_professional_blueprint_endpoint():
    """Generate professional detailed blueprint"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        print("🏗️ Generating professional blueprint...")
        
        blueprint_image = generate_professional_blueprint(data)
        
        return jsonify({
            'success': True,
            'image': blueprint_image,
            'type': 'professional_detailed'
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
        'service': 'professional_blueprint_generator'
    })

if __name__ == '__main__':
    print("=" * 70)
    print("🏗️ VASTU VISION - PROFESSIONAL BLUEPRINT GENERATOR")
    print("=" * 70)
    print("✅ Detailed dimensions for each room")
    print("✅ Professional furniture placement")
    print("✅ Doors and windows with proper representation")
    print("✅ Compass with all directions")
    print("✅ Architectural blueprint style")
    print("🌐 Server: http://localhost:5006")
    print("=" * 70)
    app.run(host='0.0.0.0', port=5006, debug=True)

