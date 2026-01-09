#!/usr/bin/env python3
"""
AI-Powered Layout Suggestion Engine
Uses GPT-4 or similar models to suggest optimal Vastu-compliant layouts
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import requests
from typing import Dict, Any, List, Optional

app = Flask(__name__)
CORS(app)

# AI Configuration
class LayoutAIConfig:
    """Configuration for AI layout suggestions"""
    
    # Azure OpenAI GPT-4 (Priority 1)
    AZURE_OPENAI_ENABLED = os.getenv('AZURE_OPENAI_ENABLED', 'false').lower() == 'true'
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT', '')
    AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY', '')
    AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4')
    
    # OpenAI API (Priority 2)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_ENABLED = bool(OPENAI_API_KEY)

# Vastu Rules Knowledge Base
VASTU_RULES = {
    "kitchen": {
        "ideal_direction": "southeast",
        "alternative": ["south", "east"],
        "avoid": ["northeast", "northwest", "center"],
        "reasoning": "Kitchen represents fire element (Agni). Southeast (Agneya) is the fire zone in Vastu. This placement ensures good health and prosperity.",
        "elements": ["fire"],
        "score_weight": 1.2
    },
    "bedroom": {
        "ideal_direction": "southwest",
        "alternative": ["south", "west"],
        "avoid": ["northeast", "east"],
        "reasoning": "Bedroom represents earth element (stability). Southwest is ideal for master bedroom as it provides stability and ensures peaceful sleep.",
        "elements": ["earth"],
        "score_weight": 1.3
    },
    "master bedroom": {
        "ideal_direction": "southwest",
        "alternative": ["south", "west"],
        "avoid": ["northeast", "east"],
        "reasoning": "Master bedroom in southwest ensures stability, strength, and good health for the head of family.",
        "elements": ["earth"],
        "score_weight": 1.5
    },
    "bathroom": {
        "ideal_direction": "northwest",
        "alternative": ["west", "north"],
        "avoid": ["northeast", "southeast", "center"],
        "reasoning": "Bathroom represents water element. Northwest placement allows water to flow out naturally. Never in northeast (holy direction).",
        "elements": ["water"],
        "score_weight": 1.1
    },
    "toilet": {
        "ideal_direction": "northwest",
        "alternative": ["west", "north"],
        "avoid": ["northeast", "southeast", "center", "southwest"],
        "reasoning": "Similar to bathroom, should be in northwest. Must never be in northeast or southwest (master bedroom area).",
        "elements": ["water"],
        "score_weight": 1.1
    },
    "puja room": {
        "ideal_direction": "northeast",
        "alternative": ["east", "north"],
        "avoid": ["southwest", "southeast", "west"],
        "reasoning": "Prayer room represents spiritual energy. Northeast (Ishanya) is the most auspicious direction for prayer and meditation.",
        "elements": ["space", "water"],
        "score_weight": 1.4
    },
    "living room": {
        "ideal_direction": "northeast",
        "alternative": ["north", "east", "northwest"],
        "avoid": ["southwest"],
        "reasoning": "Living room is for social activities. Northeast or north ensures positive energy flow and good relationships.",
        "elements": ["air", "space"],
        "score_weight": 1.0
    },
    "dining room": {
        "ideal_direction": "west",
        "alternative": ["northwest", "south"],
        "avoid": ["northeast"],
        "reasoning": "Dining room in west ensures good digestion and family harmony.",
        "elements": ["air", "fire"],
        "score_weight": 1.0
    },
    "study room": {
        "ideal_direction": "northeast",
        "alternative": ["north", "east"],
        "avoid": ["southwest", "south"],
        "reasoning": "Study room in northeast enhances concentration, learning, and wisdom.",
        "elements": ["air", "space"],
        "score_weight": 1.1
    },
    "store room": {
        "ideal_direction": "southwest",
        "alternative": ["south", "west"],
        "avoid": ["northeast"],
        "reasoning": "Store room should be in heavy zone (southwest) to maintain stability.",
        "elements": ["earth"],
        "score_weight": 0.9
    }
}

def get_vastu_suggestions(room_type: str, current_zone: Optional[str] = None) -> Dict[str, Any]:
    """Get Vastu suggestions for a room type"""
    room_key = room_type.lower().replace(" ", "_")
    if room_key not in VASTU_RULES:
        # Try to match partial
        for key, rules in VASTU_RULES.items():
            if key in room_key or room_key in key:
                room_key = key
                break
        else:
            # Default suggestions
            return {
                "ideal_direction": "northeast",
                "reasoning": "General room placement - consult Vastu expert for specific recommendations",
                "score": 75
            }
    
    rules = VASTU_RULES[room_key]
    score = 100 if current_zone and current_zone.lower() == rules["ideal_direction"] else 70
    
    return {
        "ideal_direction": rules["ideal_direction"],
        "alternative": rules["alternative"],
        "avoid": rules["avoid"],
        "reasoning": rules["reasoning"],
        "elements": rules["elements"],
        "score": score,
        "weight": rules["score_weight"]
    }

def call_azure_openai_gpt(prompt: str, system_prompt: str = "") -> Optional[str]:
    """Call Azure OpenAI GPT-4 for layout suggestions"""
    if not LayoutAIConfig.AZURE_OPENAI_ENABLED:
        return None
    
    try:
        headers = {
            "api-key": LayoutAIConfig.AZURE_OPENAI_API_KEY,
            "Content-Type": "application/json"
        }
        
        url = f"{LayoutAIConfig.AZURE_OPENAI_ENDPOINT}/openai/deployments/{LayoutAIConfig.AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2024-02-15-preview"
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result.get('choices', [{}])[0].get('message', {}).get('content')
        
    except Exception as e:
        print(f"❌ Azure OpenAI GPT error: {e}")
        return None

def call_openai_gpt(prompt: str, system_prompt: str = "") -> Optional[str]:
    """Call OpenAI GPT-4 API (fallback)"""
    if not LayoutAIConfig.OPENAI_ENABLED:
        return None
    
    try:
        headers = {
            "Authorization": f"Bearer {LayoutAIConfig.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        url = "https://api.openai.com/v1/chat/completions"
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": "gpt-4",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result.get('choices', [{}])[0].get('message', {}).get('content')
        
    except Exception as e:
        print(f"❌ OpenAI GPT error: {e}")
        return None

def generate_ai_layout_suggestions(space_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate AI-powered layout suggestions"""
    
    # Build context
    plot_size = space_data.get('plotSize', '1200 sq ft')
    room_type = space_data.get('roomType', '2bhk')
    orientation = space_data.get('orientation', 'north-facing')
    rooms = space_data.get('rooms', [])
    
    # System prompt for AI
    system_prompt = """You are a Vastu Shastra expert AI assistant. Provide specific, actionable layout suggestions based on ancient Vastu principles. 
Focus on:
1. Optimal room placements
2. Energy flow optimization
3. Five elements balance (Earth, Water, Fire, Air, Space)
4. Practical modern living considerations

Always provide reasoning for each suggestion."""
    
    # User prompt
    user_prompt = f"""Analyze this space layout request:

Plot Size: {plot_size}
Room Type: {room_type}
Orientation: {orientation}
Number of Rooms: {len(rooms)}

Current Room Layout:
{json.dumps(rooms, indent=2) if rooms else "No rooms specified yet"}

Provide:
1. Optimal room placement suggestions (which room in which direction)
2. Specific Vastu compliance recommendations
3. Energy balance improvements
4. Any corrections needed for current layout
5. Overall Vastu score prediction

Format response as structured JSON with: suggestions (array), reasoning, improvements, predicted_score."""
    
    # Try AI services
    ai_response = None
    if LayoutAIConfig.AZURE_OPENAI_ENABLED:
        ai_response = call_azure_openai_gpt(user_prompt, system_prompt)
    elif LayoutAIConfig.OPENAI_ENABLED:
        ai_response = call_openai_gpt(user_prompt, system_prompt)
    
    # Fallback to rule-based suggestions
    suggestions = []
    for room in rooms:
        room_name = room.get('name', '')
        room_zone = room.get('zone', '')
        vastu_suggest = get_vastu_suggestions(room_name, room_zone)
        
        suggestions.append({
            'room': room_name,
            'current_zone': room_zone,
            'ideal_zone': vastu_suggest['ideal_direction'],
            'alternatives': vastu_suggest['alternative'],
            'avoid': vastu_suggest['avoid'],
            'reasoning': vastu_suggest['reasoning'],
            'score': vastu_suggest['score'],
            'elements': vastu_suggest['elements']
        })
    
    # Try to parse AI response if available
    ai_suggestions = None
    if ai_response:
        try:
            # Try to extract JSON from response
            if '{' in ai_response and '}' in ai_response:
                json_start = ai_response.find('{')
                json_end = ai_response.rfind('}') + 1
                ai_suggestions = json.loads(ai_response[json_start:json_end])
        except:
            pass
    
    return {
        'suggestions': suggestions,
        'ai_enhanced': ai_response if ai_response else None,
        'ai_parsed': ai_suggestions,
        'method': 'ai_enhanced' if ai_response else 'rule_based'
    }

@app.route('/suggest_layout', methods=['POST', 'OPTIONS'])
def suggest_layout():
    """Get AI-powered layout suggestions"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        print("🧠 Received layout suggestion request")
        
        suggestions = generate_ai_layout_suggestions(data)
        
        return jsonify({
            'success': True,
            **suggestions
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/vastu_rules/<room_type>', methods=['GET'])
def get_vastu_rules(room_type: str):
    """Get Vastu rules for a specific room type"""
    suggestions = get_vastu_suggestions(room_type)
    return jsonify({
        'success': True,
        'room_type': room_type,
        **suggestions
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'service': 'ai_layout_suggester',
        'ai_enabled': (LayoutAIConfig.AZURE_OPENAI_ENABLED or LayoutAIConfig.OPENAI_ENABLED)
    })

if __name__ == '__main__':
    print("=" * 70)
    print("🧠 VASTU VISION - AI LAYOUT SUGGESTER")
    print("=" * 70)
    print(f"🔷 Azure OpenAI GPT: {'✅ Enabled' if LayoutAIConfig.AZURE_OPENAI_ENABLED else '❌ Disabled'}")
    print(f"🔷 OpenAI GPT: {'✅ Enabled' if LayoutAIConfig.OPENAI_ENABLED else '❌ Disabled'}")
    print(f"🌐 Server: http://localhost:5004")
    print("=" * 70)
    app.run(host='0.0.0.0', port=5004, debug=True)

