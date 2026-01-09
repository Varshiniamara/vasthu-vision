<?php
/**
 * REGISTER PROCESS - Works with your existing db_connect.php
 */

// Include your existing database connection
require_once 'db_connect.php';

header('Content-Type: application/json');
session_start();

// Only accept POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

try {
    // Get POST data
    $input = file_get_contents('php://input');
    $data = json_decode($input, true);
    
    // If JSON fails, try regular POST
    if ($data === null) {
        $data = $_POST;
    }
    
    // Validate required fields
    if (empty($data['firstName']) || empty($data['lastName']) || empty($data['email']) || 
        empty($data['phone']) || empty($data['gender']) || empty($data['password'])) {
        throw new Exception("All required fields must be filled");
    }
    
    // Validate email
    if (!filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
        throw new Exception("Invalid email format");
    }
    
    // Validate phone (Indian format)
    $phone_clean = preg_replace('/\s+/', '', $data['phone']);
    if (!preg_match('/^[6-9]\d{9}$/', $phone_clean)) {
        throw new Exception("Invalid phone number");
    }
    
    // Validate password match
    if ($data['password'] !== $data['confirmPassword']) {
        throw new Exception("Passwords do not match");
    }
    
    // Check if email exists
    $stmt = $conn->prepare("SELECT id FROM users WHERE email = ?");
    $stmt->bind_param("s", $data['email']);
    $stmt->execute();
    if ($stmt->get_result()->num_rows > 0) {
        throw new Exception("Email already registered");
    }
    
    // Check if phone exists
    $stmt = $conn->prepare("SELECT id FROM users WHERE phone = ?");
    $stmt->bind_param("s", $phone_clean);
    $stmt->execute();
    if ($stmt->get_result()->num_rows > 0) {
        throw new Exception("Phone number already registered");
    }
    
    // Hash password
    $password_hash = password_hash($data['password'], PASSWORD_BCRYPT);
    
    // Prepare date of birth
    $dob = !empty($data['dateOfBirth']) ? $data['dateOfBirth'] : null;
    
    // Insert user
    $stmt = $conn->prepare("
        INSERT INTO users (first_name, last_name, email, phone, gender, date_of_birth, password_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ");
    
    $stmt->bind_param("sssssss", 
        $data['firstName'],
        $data['lastName'],
        $data['email'],
        $phone_clean,
        $data['gender'],
        $dob,
        $password_hash
    );
    
    if ($stmt->execute()) {
        $user_id = $conn->insert_id;
        
        // Log activity
        $stmt = $conn->prepare("INSERT INTO activity_log (user_id, action, description, ip_address) VALUES (?, 'registration', 'User registered', ?)");
        $ip = $_SERVER['REMOTE_ADDR'];
        $stmt->bind_param("is", $user_id, $ip);
        $stmt->execute();
        
        echo json_encode([
            'success' => true,
            'message' => 'Registration successful! Please login.',
            'user_id' => $user_id
        ]);
    } else {
        throw new Exception("Registration failed");
    }
    
} catch (Exception $e) {
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'message' => $e->getMessage()
    ]);
}
?>

