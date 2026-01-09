#!/usr/bin/env python3
"""
AI Assistant Service - Natural Language to Frontend Changes
Understands user prompts and generates dynamic frontend updates
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re
from typing import Dict, Any, List

app = Flask(__name__)
CORS(app)

# AI Response Templates (Simulated AI - can be replaced with OpenAI/Claude API)
def process_user_prompt(prompt: str, current_state: Dict[str, Any]) -> Dict[str, Any]:
    """Process user prompt and generate frontend changes"""
    
    prompt_lower = prompt.lower()
    
    # Vastu-related queries
    if any(word in prompt_lower for word in ['vastu', 'placement', 'room', 'kitchen', 'bedroom', 'bathroom']):
        return handle_vastu_query(prompt, current_state)
    
    # Layout changes
    elif any(word in prompt_lower for word in ['layout', 'design', 'blueprint', 'floor plan']):
        return handle_layout_query(prompt, current_state)
    
    # Color/styling changes
    elif any(word in prompt_lower for word in ['color', 'theme', 'style', 'appearance', 'design']):
        return handle_styling_query(prompt, current_state)
    
    # Feature requests
    elif any(word in prompt_lower for word in ['add', 'feature', 'function', 'button', 'section']):
        return handle_feature_query(prompt, current_state)
    
    # Analysis requests
    elif any(word in prompt_lower for word in ['analyze', 'score', 'report', 'recommendation']):
        return handle_analysis_query(prompt, current_state)
    
    # General help
    else:
        return handle_general_query(prompt, current_state)

# Fix the handle_general_query to use prompt_lower
def handle_general_query(prompt: str, current_state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle general queries"""
    prompt_lower = prompt.lower()
    if any(word in prompt_lower for word in ['hello', 'hi', 'help']):
        return {
            'type': 'welcome',
            'message': 'Hello! I\'m your Vastu AI assistant. I can help you with:\n• Room placements\n• Layout generation\n• Vastu analysis\n• Design suggestions\n• Color themes\n\nWhat would you like to do?',
            'frontend_changes': {
                'show_help': True
            },
            'confidence': 0.8
        }
    
    return {
        'type': 'general',
        'message': 'I understand you need help. I can assist with Vastu planning, layouts, styling, and more. Try asking: "Where should I place my kitchen?" or "Generate a modern layout"',
        'frontend_changes': {},
        'confidence': 0.6
    }

def handle_vastu_query(prompt: str, current_state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle Vastu-related queries"""
    prompt_lower = prompt.lower()
    
    # Extract room type and direction
    room = None
    direction = None
    
    vastu_rules = {
        'kitchen': 'southeast',
        'bedroom': 'southwest',
        'master bedroom': 'southwest',
        'bathroom': 'northwest',
        'toilet': 'northwest',
        'living room': 'northeast',
        'puja room': 'northeast',
        'prayer room': 'northeast'
    }
    
    for room_type, optimal_zone in vastu_rules.items():
        if room_type in prompt_lower:
            room = room_type
            direction = optimal_zone
            break
    
    if room and direction:
        return {
            'type': 'vastu_recommendation',
            'message': f"According to Vastu Shastra, {room.title()} should be placed in the {direction.upper()} direction for optimal energy flow.",
            'frontend_changes': {
                'show_vastu_tip': True,
                'room': room,
                'optimal_zone': direction,
                'action': 'highlight_zone',
                'zone': direction
            },
            'confidence': 0.95
        }
    
    return {
        'type': 'info',
        'message': 'I can help you with Vastu placement for any room. Try: "Where should the kitchen be?" or "Best placement for master bedroom"',
        'frontend_changes': {},
        'confidence': 0.7
    }

def handle_layout_query(prompt: str, current_state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle layout and design queries"""
    prompt_lower = prompt.lower()
    
    if 'compact' in prompt_lower or 'small' in prompt_lower:
        return {
            'type': 'layout_change',
            'message': 'I\'ll generate a compact layout optimized for space efficiency while maintaining Vastu principles.',
            'frontend_changes': {
                'generate_blueprint': True,
                'layout_type': 'compact',
                'update_ui': 'show_blueprint_generation'
            },
            'confidence': 0.9
        }
    
    elif 'modern' in prompt_lower or 'contemporary' in prompt_lower:
        return {
            'type': 'layout_change',
            'message': 'Generating a modern layout with contemporary design elements and Vastu compliance.',
            'frontend_changes': {
                'generate_blueprint': True,
                'layout_type': 'modern',
                'update_ui': 'show_blueprint_generation'
            },
            'confidence': 0.9
        }
    
    return {
        'type': 'layout_suggestion',
        'message': 'I can generate optimal, modern, or compact layouts. What style would you prefer?',
        'frontend_changes': {
            'show_layout_options': True
        },
        'confidence': 0.8
    }

def handle_styling_query(prompt: str, current_state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle styling and appearance queries"""
    prompt_lower = prompt.lower()
    
    # Color changes
    colors = {
        'blue': '#4A90E2',
        'green': '#2A9D8F',
        'orange': '#F4A261',
        'purple': '#667eea',
        'red': '#FF6B6B',
        'dark': '#2A363B'
    }
    
    for color_name, hex_code in colors.items():
        if color_name in prompt_lower:
            return {
                'type': 'styling_change',
                'message': f'Changing theme to {color_name} color scheme.',
                'frontend_changes': {
                    'update_theme': True,
                    'primary_color': hex_code,
                    'apply_css': True
                },
                'confidence': 0.95
            }
    
    if 'dark mode' in prompt_lower or 'dark theme' in prompt_lower:
        return {
            'type': 'styling_change',
            'message': 'Switching to dark mode for better visibility.',
            'frontend_changes': {
                'update_theme': True,
                'dark_mode': True,
                'apply_css': True
            },
            'confidence': 0.95
        }
    
    return {
        'type': 'info',
        'message': 'I can change colors, themes, and styling. Try: "Make it blue" or "Switch to dark mode"',
        'frontend_changes': {},
        'confidence': 0.7
    }

def handle_feature_query(prompt: str, current_state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle feature addition requests"""
    prompt_lower = prompt.lower()
    
    if 'calculator' in prompt_lower:
        return {
            'type': 'feature_add',
            'message': 'Adding Vastu score calculator to help you analyze spaces.',
            'frontend_changes': {
                'add_component': 'vastu_calculator',
                'position': 'sidebar'
            },
            'confidence': 0.9
        }
    
    if 'comparison' in prompt_lower or 'compare' in prompt_lower:
        return {
            'type': 'feature_add',
            'message': 'Adding layout comparison tool to compare different Vastu configurations.',
            'frontend_changes': {
                'add_component': 'layout_comparison',
                'position': 'main'
            },
            'confidence': 0.9
        }
    
    return {
        'type': 'info',
        'message': 'I can add features like calculators, comparisons, and more. What would you like?',
        'frontend_changes': {},
        'confidence': 0.7
    }

def handle_analysis_query(prompt: str, current_state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle analysis and recommendation requests"""
    return {
        'type': 'analysis',
        'message': 'Generating detailed Vastu analysis with recommendations for your space.',
        'frontend_changes': {
            'trigger_analysis': True,
            'show_recommendations': True
        },
        'confidence': 0.9
    }

def handle_general_query(prompt: str, current_state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle general queries"""
    prompt_lower = prompt.lower()
    if any(word in prompt_lower for word in ['hello', 'hi', 'help']):
        return {
            'type': 'welcome',
            'message': 'Hello! I\'m your Vastu AI assistant. I can help you with:\n• Room placements\n• Layout generation\n• Vastu analysis\n• Design suggestions\n• Color themes\n\nWhat would you like to do?',
            'frontend_changes': {
                'show_help': True
            },
            'confidence': 0.8
        }
    
    return {
        'type': 'general',
        'message': 'I understand you need help. I can assist with Vastu planning, layouts, styling, and more. Try asking: "Where should I place my kitchen?" or "Generate a modern layout"',
        'frontend_changes': {},
        'confidence': 0.6
    }

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    """AI Chat endpoint"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        current_state = data.get('current_state', {})
        
        if not prompt:
            return jsonify({
                'success': False,
                'error': 'No prompt provided'
            }), 400
        
        print(f"🤖 AI Request: {prompt}")
        
        # Process prompt
        response = process_user_prompt(prompt, current_state)
        
        print(f"✅ AI Response: {response['type']}")
        
        return jsonify({
            'success': True,
            'response': response
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
        'service': 'ai_assistant',
        'version': '1.0'
    })

if __name__ == '__main__':
    print("=" * 70)
    print("🤖 VASTU VISION - AI ASSISTANT SERVICE")
    print("=" * 70)
    print("✅ Natural language processing")
    print("✅ Dynamic frontend updates")
    print("✅ Vastu recommendations")
    print("✅ Layout generation")
    print("🌐 Server: http://localhost:5008")
    print("=" * 70)
    app.run(host='0.0.0.0', port=5008, debug=True)

