# Google Maps Integration Guide - VastuVision XR

## 🗺️ Setting Up Google Maps API

VastuVision XR now uses **Google Maps JavaScript API** for interactive map visualization instead of static Mapbox images.

### Step 1: Get Your Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - **Maps JavaScript API**
   - **Places API** (optional, for advanced features)
   - **Geocoding API** (optional, for reverse geocoding)

4. Go to **Credentials** → **Create Credentials** → **API Key**
5. Copy your API key (it will look like: `AIzaSyB...`)

### Step 2: Secure Your API Key (Recommended)

1. In Google Cloud Console, click on your API key to edit it
2. Under **Application restrictions**, choose **HTTP referrers**
3. Add your domain:
   - For local development: `http://localhost:8000/*`
   - For production: `https://yourdomain.com/*`
4. Under **API restrictions**, select **Restrict key** and choose:
   - Maps JavaScript API
   - Places API (if using)

### Step 3: Replace the Placeholder in Your Code

Update the API key in the following files:

#### File 1: `space.php`
**Line 25:** Replace `YOUR_GOOGLE_MAPS_API_KEY` with your actual API key:
```html
<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_ACTUAL_API_KEY&libraries=places"></script>
```

#### File 2: `xr_space.html`
**Line 9:** Replace `YOUR_GOOGLE_MAPS_API_KEY` with your actual API key:
```html
<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_ACTUAL_API_KEY&libraries=places"></script>
```

### Step 4: Test the Integration

1. Restart your services: `./start_services.sh`
2. Open `http://localhost:8000/space.php` or `http://localhost:8000/xr_space.html`
3. Click **"Auto-Detect Location"**
4. You should see:
   - An interactive Google Map in satellite view with dark styling
   - A red marker at your detected location
   - Map controls (zoom, map type selector, street view)
   - An info window showing your coordinates

### Features Included

✅ **Interactive satellite map** with custom dark theme  
✅ **Automatic location detection** via browser Geolocation API  
✅ **Custom marker** with coordinates display  
✅ **Multiple map types**: Roadmap, Satellite, Hybrid, Terrain  
✅ **Zoom controls** and Street View integration  
✅ **Responsive design** that matches VastuVision's aesthetic  

### Troubleshooting

**Issue**: Map not loading / Gray screen
- **Fix**: Check browser console for errors. Ensure API key is valid and Maps JavaScript API is enabled.

**Issue**: "RefererNotAllowedMapError"
- **Fix**: Add your domain to the API key's HTTP referrer restrictions in Google Cloud Console.

**Issue**: "This page can't load Google Maps correctly"
- **Fix**: Verify billing is enabled on your Google Cloud project (free tier includes $200/month credit).

### Cost Information

Google Maps provides:
- **$200 free credit per month** (covers ~28,000 map loads)
- After free tier: ~$7 per 1,000 map loads
- For most development/demo purposes, you'll stay within the free tier

### Alternative Options

If you prefer not to use Google Maps, you can:
1. Use **Leaflet.js** with OpenStreetMap (completely free)
2. Use **Mapbox GL JS** (also has a generous free tier)

Contact the development team if you need help with alternative integrations.

---
**Status**: Google Maps Integration Complete ✅  
**Last Updated**: January 2026
