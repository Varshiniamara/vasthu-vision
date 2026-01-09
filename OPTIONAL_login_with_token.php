<?php
/**
 * LOGIN WITH API TOKEN (Optional Enhancement)
 * Generates API token for mobile apps or external access
 */

require_once 'db_connect.php';

header('Content-Type: application/json');
session_start();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

try {
    $input = file_get_contents('php://input');
    $data = json_decode($input, true);
    
    if ($data === null) {
        $data = $_POST;
    }
    
    if (empty($data['email']) || empty($data['password'])) {
        throw new Exception("Email and password are required");
    }
    
    // Get user
    $stmt = $conn->prepare("
        SELECT id, first_name, last_name, email, password_hash, is_active
        FROM users
        WHERE email = ?
    ");
    $stmt->bind_param("s", $data['email']);
    $stmt->execute();
    $result = $stmt->get_result();
    $user = $result->fetch_assoc();
    
    if (!$user || !password_verify($data['password'], $user['password_hash'])) {
        throw new Exception("Invalid email or password");
    }
    
    if (!$user['is_active']) {
        throw new Exception("Account is deactivated");
    }
    
    // Generate API token
    $api_token = bin2hex(random_bytes(32)); // 64 character token
    
    // Save token to database
    $stmt = $conn->prepare("UPDATE users SET api_token = ? WHERE id = ?");
    $stmt->bind_param("si", $api_token, $user['id']);
    $stmt->execute();
    
    // Update last login
    $stmt = $conn->prepare("UPDATE users SET last_login = NOW() WHERE id = ?");
    $stmt->bind_param("i", $user['id']);
    $stmt->execute();
    
    // Create session (for web)
    $_SESSION['logged_in'] = true;
    $_SESSION['user_id'] = $user['id'];
    $_SESSION['user_name'] = $user['first_name'] . ' ' . $user['last_name'];
    $_SESSION['user_email'] = $user['email'];
    
    // Log activity
    $stmt = $conn->prepare("INSERT INTO activity_log (user_id, action, description, ip_address) VALUES (?, 'login', 'User logged in with token', ?)");
    $ip = $_SERVER['REMOTE_ADDR'];
    $stmt->bind_param("is", $user['id'], $ip);
    $stmt->execute();
    
    echo json_encode([
        'success' => true,
        'message' => 'Login successful!',
        'redirect' => 'dashboard.php',
        'api_token' => $api_token, // Return token for mobile/API use
        'user' => [
            'id' => $user['id'],
            'name' => $user['first_name'] . ' ' . $user['last_name'],
            'email' => $user['email']
        ]
    ]);
    
} catch (Exception $e) {
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'message' => $e->getMessage()
    ]);
}
?>

