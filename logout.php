<?php
/**
 * User Logout
 * Handles user logout and session cleanup
 */

require_once 'config.php';
require_once 'Database.php';

// Log activity before destroying session
if (isset($_SESSION['user_id'])) {
    try {
        $db = Database::getInstance()->getConnection();
        $stmt = $db->prepare("
            INSERT INTO activity_log (user_id, action, description, ip_address)
            VALUES (?, 'user_logout', 'User logged out', ?)
        ");
        $stmt->execute([$_SESSION['user_id'], $_SERVER['REMOTE_ADDR']]);
    } catch (Exception $e) {
        error_log("Logout logging error: " . $e->getMessage());
    }
}

// Clear remember me cookie if exists
if (isset($_COOKIE['remember_token'])) {
    setcookie('remember_token', '', time() - 3600, '/', '', true, true);
}

// Destroy session
session_unset();
session_destroy();

// Redirect to login page
header('Location: login.html');
exit;
?>

