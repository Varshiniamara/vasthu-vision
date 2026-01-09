#!/usr/bin/env python3
"""
AI-Powered Blueprint Generator Service
Integrates with Azure OpenAI (DALL-E) and fallback options for blueprint generation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import base64
import requests
from typing import Optional, Dict, Any

app = Flask(__name__)
CORS(app)

# AI Service Configuration
class AIServiceConfig:
    """Configuration for AI services"""
    
    # Azure OpenAI Configuration (Priority 1)
    AZURE_OPENAI_ENABLED = os.getenv('AZURE_OPENAI_ENABLED', 'false').lower() == 'true'
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT', '')
    AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY', '')
    AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'dall-e-3')
    
    # OpenAI API (Priority 2)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_ENABLED = bool(OPENAI_API_KEY)
    
    # Hugging Face (Priority 3 - Free tier)
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '')
    HUGGINGFACE_ENABLED = bool(HUGGINGFACE_API_KEY)
    
    # Stability AI (Priority 4)
    STABILITY_API_KEY = os.getenv('STABILITY_API_KEY', '')
    STABILITY_ENABLED = bool(STABILITY_API_KEY)

def generate_vastu_prompt(space_data: Dict[str, Any]) -> str:
    """
    Generate AI prompt for blueprint generation based on Vastu rules
    """
    plot_size = space_data.get('plotSize', '1200 sq ft')
    room_type = space_data.get('roomType', '2bhk')
    orientation = space_data.get('orientation', 'north-facing').replace('-', ' ')
    floor_number = space_data.get('floorNumber', '1')
    rooms = space_data.get('rooms', [])
    
    # Vastu Rules Mapping
    vastu_rules = {
        'kitchen': 'southeast',
        'bedroom': 'southwest',
        'master bedroom': 'southwest',
        'bathroom': 'northwest',
        'toilet': 'northwest',
        'puja room': 'northeast',
        'prayer room': 'northeast',
        'living room': 'northeast or northwest',
        'hall': 'northeast or northwest',
        'dining room': 'west or northwest',
        'study room': 'northeast',
        'store room': 'southwest'
    }
    
    # Extract room placements from user input
    room_placements = []
    for room in rooms:
        room_name = room.get('name', '').lower()
        room_zone = room.get('zone', '').lower()
        room_placements.append(f"{room_name} in {room_zone}")
    
    # Build comprehensive prompt
    prompt = f"""Generate a professional 2D architectural floor plan blueprint of a {room_type.upper()} flat/house.

SPECIFICATIONS:
- Plot size: {plot_size}
- Main entrance facing: {orientation}
- Floor number: {floor_number}
- Total rooms: {len(rooms)} rooms

VASTU COMPLIANCE RULES:
- Kitchen must be in Southeast direction
- Master bedroom should be in Southwest
- Bathroom/Toilet in Northwest
- Prayer/Puja room in Northeast
- Living room in Northeast or Northwest
- Dining room in West or Northwest
- Store room in Southwest
- Keep center area open/clear

ROOM PLACEMENTS:
{chr(10).join(f"- {placement}" for placement in room_placements) if room_placements else "- Optimize room placements according to Vastu principles"}

REQUIREMENTS:
- Show all rooms with labels
- Include doors and windows
- Show furniture layout (beds, tables, kitchen counters)
- Add dimensions for each room
- Use architectural blueprint style (black lines on white background)
- Include compass direction indicator
- Show main entrance clearly
- Keep layout realistic and functional
- No blank spaces, all areas should be utilized
- Professional architectural drawing style
- Scale indicator

STYLE: Clean, professional architectural blueprint, top-down view, 2D floor plan, technical drawing style."""
    
    return prompt

def call_azure_openai(prompt: str, model: str = "dall-e-3") -> Optional[str]:
    """Call Azure OpenAI DALL-E API"""
    if not AIServiceConfig.AZURE_OPENAI_ENABLED:
        return None
    
    try:
        headers = {
            "api-key": AIServiceConfig.AZURE_OPENAI_API_KEY,
            "Content-Type": "application/json"
        }
        
        url = f"{AIServiceConfig.AZURE_OPENAI_ENDPOINT}/openai/deployments/{model}/images/generations?api-version=2024-02-15-preview"
        
        payload = {
            "prompt": prompt,
            "size": "1024x1024",
            "n": 1,
            "quality": "standard"
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        image_url = result.get('data', [{}])[0].get('url')
        
        if image_url:
            # Download image and convert to base64
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()
            return base64.b64encode(img_response.content).decode('utf-8')
            
    except Exception as e:
        print(f"❌ Azure OpenAI error: {e}")
        return None
    
    return None

def call_openai_api(prompt: str, model: str = "dall-e-3") -> Optional[str]:
    """Call OpenAI DALL-E API (fallback)"""
    if not AIServiceConfig.OPENAI_ENABLED:
        return None
    
    try:
        headers = {
            "Authorization": f"Bearer {AIServiceConfig.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        url = "https://api.openai.com/v1/images/generations"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "size": "1024x1024",
            "n": 1,
            "quality": "standard"
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        image_url = result.get('data', [{}])[0].get('url')
        
        if image_url:
            # Download image and convert to base64
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()
            return base64.b64encode(img_response.content).decode('utf-8')
            
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        return None
    
    return None

def call_huggingface_api(prompt: str) -> Optional[str]:
    """Call Hugging Face Stable Diffusion API (free tier fallback)"""
    if not AIServiceConfig.HUGGINGFACE_ENABLED:
        return None
    
    try:
        headers = {
            "Authorization": f"Bearer {AIServiceConfig.HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Using a free Stable Diffusion model
        url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
        
        payload = {
            "inputs": prompt,
            "options": {"wait_for_model": True}
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        # Return as base64
        return base64.b64encode(response.content).decode('utf-8')
        
    except Exception as e:
        print(f"❌ Hugging Face API error: {e}")
        return None
    
    return None

def generate_ai_blueprint(space_data: Dict[str, Any]) -> Optional[str]:
    """
    Generate blueprint using AI services in priority order
    """
    prompt = generate_vastu_prompt(space_data)
    print(f"🤖 Generated AI prompt: {prompt[:200]}...")
    
    # Try Azure OpenAI first (Microsoft hackathon alignment)
    if AIServiceConfig.AZURE_OPENAI_ENABLED:
        print("🔷 Attempting Azure OpenAI...")
        result = call_azure_openai(prompt)
        if result:
            print("✅ Blueprint generated via Azure OpenAI!")
            return result
    
    # Try OpenAI API
    if AIServiceConfig.OPENAI_ENABLED:
        print("🔷 Attempting OpenAI API...")
        result = call_openai_api(prompt)
        if result:
            print("✅ Blueprint generated via OpenAI!")
            return result
    
    # Try Hugging Face (free)
    if AIServiceConfig.HUGGINGFACE_ENABLED:
        print("🔷 Attempting Hugging Face...")
        result = call_huggingface_api(prompt)
        if result:
            print("✅ Blueprint generated via Hugging Face!")
            return result
    
    print("⚠️ No AI service available or all failed")
    return None

@app.route('/generate_ai_blueprint', methods=['POST', 'OPTIONS'])
def generate_ai_blueprint_endpoint():
    """Generate AI-powered blueprint"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        print("🤖 Received AI blueprint generation request")
        
        # Generate blueprint using AI
        blueprint_image = generate_ai_blueprint(data)
        
        if blueprint_image:
            return jsonify({
                'success': True,
                'image': blueprint_image,
                'prompt_used': generate_vastu_prompt(data)[:200] + "...",
                'service': 'ai_generated'
            })
        else:
            # Fallback to procedural generation
            return jsonify({
                'success': False,
                'error': 'AI services not configured. Please set up API keys or use procedural generation.',
                'fallback_available': True,
                'fallback_endpoint': 'http://localhost:5002/generate_blueprints'
            }), 503
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/ai_status', methods=['GET'])
def ai_status():
    """Check AI service status"""
    return jsonify({
        'azure_openai': AIServiceConfig.AZURE_OPENAI_ENABLED,
        'openai': AIServiceConfig.OPENAI_ENABLED,
        'huggingface': AIServiceConfig.HUGGINGFACE_ENABLED,
        'stability': AIServiceConfig.STABILITY_ENABLED,
        'services_available': (
            AIServiceConfig.AZURE_OPENAI_ENABLED or
            AIServiceConfig.OPENAI_ENABLED or
            AIServiceConfig.HUGGINGFACE_ENABLED or
            AIServiceConfig.STABILITY_ENABLED
        )
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'service': 'ai_blueprint_service',
        'ai_enabled': (
            AIServiceConfig.AZURE_OPENAI_ENABLED or
            AIServiceConfig.OPENAI_ENABLED or
            AIServiceConfig.HUGGINGFACE_ENABLED
        )
    })

if __name__ == '__main__':
    print("=" * 70)
    print("🤖 VASTU VISION - AI BLUEPRINT GENERATOR SERVICE")
    print("=" * 70)
    print(f"🔷 Azure OpenAI: {'✅ Enabled' if AIServiceConfig.AZURE_OPENAI_ENABLED else '❌ Disabled'}")
    print(f"🔷 OpenAI API: {'✅ Enabled' if AIServiceConfig.OPENAI_ENABLED else '❌ Disabled'}")
    print(f"🔷 Hugging Face: {'✅ Enabled' if AIServiceConfig.HUGGINGFACE_ENABLED else '❌ Disabled'}")
    print(f"🌐 Server: http://localhost:5003")
    print("=" * 70)
    app.run(host='0.0.0.0', port=5003, debug=True)

