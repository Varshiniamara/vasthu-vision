# 🤖 AI Services Configuration Guide

This guide explains how to configure AI-powered features for Vastu Vision.

## 📋 Available AI Services

1. **AI Blueprint Generator** (Port 5003) - DALL-E/Stable Diffusion integration
2. **AI Layout Suggester** (Port 5004) - GPT-4 powered layout recommendations
3. **Energy Heatmap Generator** (Port 5005) - Visual energy balance mapping

---

## 🔑 Setting Up API Keys

### Option 1: Azure OpenAI (Recommended for Microsoft Hackathon) ⭐

Since this is a Microsoft hackathon, Azure OpenAI is the perfect choice!

#### Steps:
1. Go to [Azure Portal](https://portal.azure.com)
2. Create an Azure OpenAI resource
3. Deploy a model (DALL-E-3 for images, GPT-4 for text)
4. Get your endpoint URL and API key

#### Set Environment Variables:
```bash
# Windows PowerShell
$env:AZURE_OPENAI_ENABLED="true"
$env:AZURE_OPENAI_ENDPOINT="https://YOUR-RESOURCE.openai.azure.com"
$env:AZURE_OPENAI_API_KEY="your-api-key-here"
$env:AZURE_OPENAI_DEPLOYMENT="dall-e-3"  # or "gpt-4" for layout suggestions
```

```bash
# Windows CMD
set AZURE_OPENAI_ENABLED=true
set AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com
set AZURE_OPENAI_API_KEY=your-api-key-here
set AZURE_OPENAI_DEPLOYMENT=dall-e-3
```

### Option 2: OpenAI API (Direct)

If you have an OpenAI API key:

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your-openai-api-key"

# Windows CMD
set OPENAI_API_KEY=your-openai-api-key
```

### Option 3: Hugging Face (Free Tier)

Get free API key from [Hugging Face](https://huggingface.co/settings/tokens):

```bash
# Windows PowerShell
$env:HUGGINGFACE_API_KEY="your-huggingface-token"

# Windows CMD
set HUGGINGFACE_API_KEY=your-huggingface-token
```

### Option 4: Stability AI

For Stable Diffusion:

```bash
# Windows PowerShell
$env:STABILITY_API_KEY="your-stability-api-key"

# Windows CMD
set STABILITY_API_KEY=your-stability-api-key
```

---

## 🚀 Quick Start (Without API Keys)

**Good news!** All AI services work without API keys using fallback methods:

- **AI Blueprint**: Falls back to procedural generation (Port 5002)
- **AI Layout**: Uses rule-based Vastu suggestions
- **Energy Heatmap**: Works independently (no API needed)

You can test everything immediately! API keys just enable enhanced AI features.

---

## 📝 Creating a `.env` File (Alternative)

Create a `.env` file in the project root:

```env
# Azure OpenAI (Recommended for Microsoft Hackathon)
AZURE_OPENAI_ENABLED=true
AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT=dall-e-3

# OpenAI API (Fallback)
OPENAI_API_KEY=your-openai-api-key

# Hugging Face (Free Tier)
HUGGINGFACE_API_KEY=your-huggingface-token

# Stability AI
STABILITY_API_KEY=your-stability-api-key
```

**Note:** Python Flask apps need `python-dotenv` to read `.env` files:
```bash
pip install python-dotenv
```

Then update the Python files to load from `.env`:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 🧪 Testing AI Services

### 1. Check Service Status

Visit these URLs after starting servers:

- AI Blueprint Status: `http://localhost:5003/ai_status`
- AI Layout Status: `http://localhost:5004/health`
- Energy Heatmap Status: `http://localhost:5005/health`

### 2. Test from Frontend

Open: `http://localhost:8000/ai_features_page.html`

This page allows you to:
- Generate AI blueprints
- Get layout suggestions
- View energy heatmaps

### 3. Test via API

```bash
# Test AI Blueprint
curl -X POST http://localhost:5003/generate_ai_blueprint \
  -H "Content-Type: application/json" \
  -d '{"plotSize": "2800 sq ft", "roomType": "2bhk", "orientation": "north-facing", "rooms": []}'

# Test Layout Suggestions
curl -X POST http://localhost:5004/suggest_layout \
  -H "Content-Type: application/json" \
  -d '{"plotSize": "2800 sq ft", "roomType": "2bhk", "rooms": [{"name": "Kitchen", "zone": "southeast"}]}'

# Test Energy Heatmap
curl -X POST http://localhost:5005/generate_heatmap \
  -H "Content-Type: application/json" \
  -d '{"plotSize": "2800 sq ft", "rooms": [{"name": "Kitchen", "zone": "southeast"}]}'
```

---

## 🎯 Priority Order

AI services try APIs in this order:

1. **Azure OpenAI** (if configured)
2. **OpenAI API** (if configured)
3. **Hugging Face** (if configured)
4. **Stability AI** (if configured)
5. **Fallback methods** (always available)

---

## 💡 Tips

1. **For Microsoft Hackathon**: Use Azure OpenAI for maximum alignment
2. **Free Testing**: Use Hugging Face free tier
3. **Best Results**: Azure OpenAI DALL-E-3 for blueprints, GPT-4 for suggestions
4. **No Keys Needed**: Everything works with fallbacks for demo purposes

---

## 🔒 Security Notes

- **Never commit API keys to Git**
- Add `.env` to `.gitignore`
- Use environment variables in production
- Rotate keys regularly

---

## ❓ Troubleshooting

### "AI service not available"
- Check if the server is running on the correct port
- Verify API keys are set correctly
- Check console logs for errors

### "Generation failed"
- API key might be invalid
- Check API quota/limits
- Try fallback methods

### "Connection timeout"
- Check internet connection
- Verify API endpoint URLs
- Some services may have rate limits

---

## 📞 Support

For issues:
1. Check server console logs
2. Verify API keys are correct
3. Test fallback methods work
4. Check network connectivity

**Remember**: All features work without API keys using fallback methods!

