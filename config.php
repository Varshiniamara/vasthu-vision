<?php
/**
 * Database Configuration File
 * Vastu Vision - Backend Configuration
 */

// Database Configuration
define('DB_HOST', 'localhost');          // Your database host
define('DB_NAME', 'vastu_vision');       // Your database name
define('DB_USER', 'root');               // Your database username
define('DB_PASS', '');                   // Your database password
define('DB_CHARSET', 'utf8mb4');

// Site Configuration
define('SITE_URL', 'https://vastology.purlyedit.in');
define('SITE_NAME', 'Vastu Vision');

// File Upload Configuration
define('UPLOAD_DIR', __DIR__ . '/uploads/');
define('MAX_FILE_SIZE', 5 * 1024 * 1024); // 5MB
define('ALLOWED_FILE_TYPES', ['image/jpeg', 'image/jpg', 'image/png', 'application/pdf']);

// Session Configuration
define('SESSION_LIFETIME', 86400); // 24 hours
define('SESSION_NAME', 'vastu_session');

// Security
define('PASSWORD_MIN_LENGTH', 8);
define('HASH_ALGO', PASSWORD_BCRYPT);
define('HASH_COST', 12);

// Error Reporting (Set to 0 in production)
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Timezone
date_default_timezone_set('Asia/Kolkata');

// Create uploads directory if it doesn't exist
if (!file_exists(UPLOAD_DIR)) {
    mkdir(UPLOAD_DIR, 0755, true);
}

// Start session with custom settings
ini_set('session.cookie_httponly', 1);
ini_set('session.use_only_cookies', 1);
ini_set('session.cookie_secure', 1); // Set to 1 if using HTTPS
session_name(SESSION_NAME);

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
?>

