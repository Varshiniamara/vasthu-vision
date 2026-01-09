<?php
/**
 * API TOKEN VERIFICATION (Optional)
 * Include this in your API endpoints to verify tokens
 */

require_once 'db_connect.php';

function verifyApiToken() {
    global $conn;
    
    // Get token from header
    $headers = getallheaders();
    $token = null;
    
    // Check Authorization header
    if (isset($headers['Authorization'])) {
        $token = str_replace('Bearer ', '', $headers['Authorization']);
    }
    
    // Check X-API-Token header
    if (!$token && isset($headers['X-API-Token'])) {
        $token = $headers['X-API-Token'];
    }
    
    // Check query parameter
    if (!$token && isset($_GET['api_token'])) {
        $token = $_GET['api_token'];
    }
    
    if (!$token) {
        http_response_code(401);
        echo json_encode(['success' => false, 'message' => 'API token required']);
        exit;
    }
    
    // Verify token
    $stmt = $conn->prepare("
        SELECT id, first_name, last_name, email, is_active
        FROM users
        WHERE api_token = ?
    ");
    $stmt->bind_param("s", $token);
    $stmt->execute();
    $result = $stmt->get_result();
    $user = $result->fetch_assoc();
    
    if (!$user) {
        http_response_code(401);
        echo json_encode(['success' => false, 'message' => 'Invalid API token']);
        exit;
    }
    
    if (!$user['is_active']) {
        http_response_code(403);
        echo json_encode(['success' => false, 'message' => 'Account deactivated']);
        exit;
    }
    
    return $user;
}

// Usage example:
// $user = verifyApiToken();
// Now you have authenticated user data
?>

