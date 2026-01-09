<?php
/**
 * User Login Processing
 * Handles user authentication
 */

require_once 'config.php'; // config.php already starts session
require_once 'Database.php';

header('Content-Type: application/json');

// Only accept POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

try {
    // Get POST data
    $data = json_decode(file_get_contents('php://input'), true);
    
    // If JSON decode fails, try regular POST
    if ($data === null) {
        $data = $_POST;
    }
    
    // Validate required fields
    if (empty($data['email']) || empty($data['password'])) {
        throw new Exception("Email and password are required");
    }
    
    // Validate email format
    if (!filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
        throw new Exception("Invalid email format");
    }
    
    // Get database connection
    $db = Database::getInstance()->getConnection();
    
    // Get user by email
    $stmt = $db->prepare("
        SELECT id, first_name, last_name, email, phone, gender, password_hash, is_active
        FROM users
        WHERE email = ?
    ");
    $stmt->execute([$data['email']]);
    $user = $stmt->fetch();
    
    if (!$user) {
        throw new Exception("Invalid email or password");
    }
    
    // Check if account is active
    if (!$user['is_active']) {
        throw new Exception("Account is deactivated. Please contact support.");
    }
    
    // Verify password
    if (!password_verify($data['password'], $user['password_hash'])) {
        throw new Exception("Invalid email or password");
    }
    
    // Update last login
    $stmt = $db->prepare("UPDATE users SET last_login = NOW() WHERE id = ?");
    $stmt->execute([$user['id']]);
    
    // Create session
    $_SESSION['logged_in'] = true;
    $_SESSION['user_id'] = $user['id'];
    $_SESSION['user_name'] = $user['first_name'] . ' ' . $user['last_name'];
    $_SESSION['user_email'] = $user['email'];
    $_SESSION['login_time'] = time();
    
    // Remember me functionality
    if (!empty($data['rememberMe'])) {
        $token = bin2hex(random_bytes(32));
        $expires = date('Y-m-d H:i:s', strtotime('+30 days'));
        
        $stmt = $db->prepare("
            INSERT INTO user_sessions (user_id, session_token, ip_address, user_agent, expires_at)
            VALUES (?, ?, ?, ?, ?)
        ");
        $stmt->execute([
            $user['id'],
            $token,
            $_SERVER['REMOTE_ADDR'],
            $_SERVER['HTTP_USER_AGENT'] ?? '',
            $expires
        ]);
        
        // Set cookie
        setcookie('remember_token', $token, strtotime('+30 days'), '/', '', true, true);
    }
    
    // Log activity
    $stmt = $db->prepare("
        INSERT INTO activity_log (user_id, action, description, ip_address)
        VALUES (?, 'user_login', 'User logged in successfully', ?)
    ");
    $stmt->execute([$user['id'], $_SERVER['REMOTE_ADDR']]);
    
    // Return success
    echo json_encode([
        'success' => true,
        'message' => 'Login successful!',
        'redirect' => 'dashboard.php',
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
} catch (PDOException $e) {
    error_log("Database Error: " . $e->getMessage());
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Server error. Please try again later.'
    ]);
}
?>

