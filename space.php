<?php
// 1. Start the session
session_start();

// 2. Check if the user is logged in
if (!isset($_SESSION['logged_in']) || $_SESSION['logged_in'] !== true) {
    // If not logged in, redirect to login page
    header('Location: login.php');
    exit;
}

// Retrieve user info from session
$user_name = $_SESSION['user_name'] ?? 'User';
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Space Details - Vastu Vision</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="space-styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo">
                <i class="fas fa-home"></i>
                <span>Vastu Vision</span>
            </div>
            <ul class="nav-menu">
                <li><a href="index.html">Home</a></li>
                <li><a href="index.html#features">Features</a></li>
                <li><a href="index.html#about">About</a></li>
                <li><a href="index.html#contact">Contact</a></li>
            </ul>
            <div class="nav-buttons">
                <span class="user-greeting">
                    <i class="fas fa-user-circle"></i>
                    Hello, <?php echo htmlspecialchars($user_name); ?>
                </span>
                <a href="logout.php" class="btn-logout">Logout</a>
                <a href="dashboard.php" class="btn-dashboard">Dashboard</a>
            </div>
            <div class="nav-toggle">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    </nav>

    <!-- Space Details Section -->
    <section class="space-section">
        <div class="space-container">
            <div class="space-header">
                <div class="space-icon">
                    <i class="fas fa-edit"></i>
                </div>
                <h1>Space Details</h1>
                <p>Enter your space details for Vastu analysis</p>
            </div>

            <div class="space-form-container">
                <form class="space-form" id="spaceForm">
                    <div class="form-section">
                        <h3><i class="fas fa-globe"></i> Geospatial Intelligence</h3>
                        <p style="font-size: 0.9rem; color: #778899; margin-bottom: 1.5rem;">Initialize with precise environmental data for advanced Vastu analysis.</p>
                        
                        <div class="geo-controls" style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px;">
                            <button type="button" class="btn-geo" onclick="detectLocation()" style="background: var(--deep-green); color: white; border: none; padding: 10px; border-radius: 8px; cursor: pointer;">
                                <i class="fas fa-location-crosshairs"></i> Auto-Detect Location
                            </button>
                            <button type="button" class="btn-geo" onclick="fetchEnvironmentDataManual()" style="background: var(--accent); color: white; border: none; padding: 10px; border-radius: 8px; cursor: pointer;">
                                <i class="fas fa-satellite-dish"></i> Environmental Scan
                            </button>
                        </div>

                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 20px;">
                            <div class="form-group">
                                <label for="lat">Latitude</label>
                                <input type="text" id="lat" name="lat" placeholder="0.000000" readonly style="background: #f0f0f0;">
                            </div>
                            <div class="form-group">
                                <label for="lng">Longitude</label>
                                <input type="text" id="lng" name="lng" placeholder="0.000000" readonly style="background: #f0f0f0;">
                            </div>
                            <div class="form-group">
                                <label for="elevation">Elevation (m)</label>
                                <input type="text" id="elevation" name="elevation" placeholder="N/A" readonly style="background: #f0f0f0;">
                            </div>
                        </div>

                        <div id="mapContainer" style="height: 250px; background: #eee; border-radius: 12px; margin-bottom: 20px; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center; border: 1px solid #ddd;">
                            <div id="mapPlaceholder" style="text-align: center; color: #999;">
                                <i class="fas fa-map-marked-alt" style="font-size: 3rem; margin-bottom: 10px;"></i>
                                <p>Map will appear here after location detection</p>
                            </div>
                            <img id="mapView" src="" alt="Map View" style="display: none; width: 100%; height: 100%; object-fit: cover;">
                        </div>

                        <div id="envInfo" style="display: none; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px;">
                            <div style="background: #fdf6e3; padding: 10px; border-radius: 8px; border-left: 4px solid var(--primary); font-size: 0.85rem;">
                                <strong>True North:</strong> <span id="trueNorthDev">--</span>
                            </div>
                            <div style="background: #fdf6e3; padding: 10px; border-radius: 8px; border-left: 4px solid var(--accent); font-size: 0.85rem;">
                                <strong>Sunrise Azimuth:</strong> <span id="sunriseAz">--</span>
                            </div>
                        </div>
                    </div>

                    <div class="form-section">
                        <h3><i class="fas fa-home"></i> Space Details</h3>
                        
                        <div class="form-group">
                            <label for="plotSize">Plot Size *</label>
                            <input type="text" id="plotSize" name="plotSize" required placeholder="e.g., 1200 sq ft">
                            <span class="error-message" id="plotSizeError"></span>
                        </div>

                        <div class="form-group">
                            <label for="roomType">Room Type *</label>
                            <select id="roomType" name="roomType" required>
                                <option value="">Select Room Type</option>
                                <option value="1bhk">1 BHK</option>
                                <option value="2bhk">2 BHK</option>
                                <option value="3bhk">3 BHK</option>
                                <option value="4bhk">4 BHK</option>
                                <option value="5bhk">5 BHK</option>
                                <option value="studio">Studio</option>
                                <option value="duplex">Duplex</option>
                                <option value="penthouse">Penthouse</option>
                            </select>
                            <span class="error-message" id="roomTypeError"></span>
                        </div>

                        <div class="form-group">
                            <label for="roomNames">Rooms & Zones *</label>
                            <div class="room-names-container" id="roomNamesContainer">
                                <div class="room-name-item">
                                    <div class="room-input-wrapper">
                                        <input type="text" name="roomNames[]" required placeholder="e.g., Living Room" class="room-name-input">
                                        <select name="roomZones[]" required class="room-zone-select">
                                            <option value="">Select Zone</option>
                                            <option value="north">North</option>
                                            <option value="northeast">Northeast</option>
                                            <option value="east">East</option>
                                            <option value="southeast">Southeast</option>
                                            <option value="south">South</option>
                                            <option value="southwest">Southwest</option>
                                            <option value="west">West</option>
                                            <option value="northwest">Northwest</option>
                                            <option value="center">Center</option>
                                        </select>
                                    </div>
                                    <button type="button" class="remove-room" onclick="removeRoomName(this)" style="display: none;">
                                        <i class="fas fa-times"></i>
                                    </button>
                                </div>
                            </div>
                            <button type="button" class="btn-add-room" onclick="addRoomName()">
                                <i class="fas fa-plus"></i>
                                Add Another Room
                            </button>
                            <span class="error-message" id="roomNamesError"></span>
                        </div>

                        <div class="form-group">
                            <label for="orientation">Orientation *</label>
                            <select id="orientation" name="orientation" required>
                                <option value="">Select Orientation</option>
                                <option value="north-facing">North Facing</option>
                                <option value="northeast-facing">Northeast Facing</option>
                                <option value="east-facing">East Facing</option>
                                <option value="southeast-facing">Southeast Facing</option>
                                <option value="south-facing">South Facing</option>
                                <option value="southwest-facing">Southwest Facing</option>
                                <option value="west-facing">West Facing</option>
                                <option value="northwest-facing">Northwest Facing</option>
                            </select>
                            <span class="error-message" id="orientationError"></span>
                        </div>

                        <div class="form-group">
                            <label for="floorNumber">Floor Number *</label>
                            <input type="number" id="floorNumber" name="floorNumber" required min="0" max="100" placeholder="e.g., 3">
                            <span class="error-message" id="floorNumberError"></span>
                        </div>
                    </div>

                    <div class="form-actions">
                        <button type="submit" class="btn-primary large">
                            <i class="fas fa-save"></i>
                            Save Space Details
                        </button>
                        <button type="button" class="btn-secondary" onclick="window.location.href='dashboard.php'">
                            <i class="fas fa-arrow-left"></i>
                            Back to Dashboard
                        </button>
                    </div>
                </form>
            </div>

            <!-- Saved Data Display -->
            <div class="saved-data-section" id="savedData" style="display: none;">
                <div class="saved-data-header">
                    <h2><i class="fas fa-check-circle"></i> Saved Data</h2>
                    <p>Your space details have been saved successfully</p>
                </div>
                <div class="data-display" id="dataDisplay">
                    <!-- Data will be displayed here -->
                </div>
            </div>
        </div>
    </section>

    <script src="space-script.js"></script>
</body>
</html>

