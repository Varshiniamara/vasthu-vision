<?php
/**
 * User Registration Processing
 * Handles user registration with validation
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
    $required_fields = ['firstName', 'lastName', 'email', 'phone', 'gender', 'password', 'confirmPassword'];
    foreach ($required_fields as $field) {
        if (empty($data[$field])) {
            throw new Exception("Field '$field' is required");
        }
    }
    
    // Validate email
    if (!filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
        throw new Exception("Invalid email format");
    }
    
    // Validate phone number (Indian format)
    if (!preg_match('/^[6-9]\d{9}$/', preg_replace('/\s+/', '', $data['phone']))) {
        throw new Exception("Invalid phone number format");
    }
    
    // Validate password match
    if ($data['password'] !== $data['confirmPassword']) {
        throw new Exception("Passwords do not match");
    }
    
    // Validate password strength
    if (strlen($data['password']) < PASSWORD_MIN_LENGTH) {
        throw new Exception("Password must be at least " . PASSWORD_MIN_LENGTH . " characters");
    }
    
    // Get database connection
    $db = Database::getInstance()->getConnection();
    
    // Check if email already exists
    $stmt = $db->prepare("SELECT id FROM users WHERE email = ?");
    $stmt->execute([$data['email']]);
    if ($stmt->fetch()) {
        throw new Exception("Email already registered");
    }
    
    // Check if phone already exists
    $phone_clean = preg_replace('/\s+/', '', $data['phone']);
    $stmt = $db->prepare("SELECT id FROM users WHERE phone = ?");
    $stmt->execute([$phone_clean]);
    if ($stmt->fetch()) {
        throw new Exception("Phone number already registered");
    }
    
    // Hash password
    $password_hash = password_hash($data['password'], HASH_ALGO, ['cost' => HASH_COST]);
    
    // Prepare date of birth (if provided)
    $dob = !empty($data['dateOfBirth']) ? $data['dateOfBirth'] : null;
    
    // Insert user
    $stmt = $db->prepare("
        INSERT INTO users (first_name, last_name, email, phone, gender, date_of_birth, password_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ");
    
    $result = $stmt->execute([
        $data['firstName'],
        $data['lastName'],
        $data['email'],
        $phone_clean,
        $data['gender'],
        $dob,
        $password_hash
    ]);
    
    if ($result) {
        $user_id = $db->lastInsertId();
        
        // Log activity
        $stmt = $db->prepare("
            INSERT INTO activity_log (user_id, action, description, ip_address)
            VALUES (?, 'user_registration', 'User registered successfully', ?)
        ");
        $stmt->execute([$user_id, $_SERVER['REMOTE_ADDR']]);
        
        // Return success
        echo json_encode([
            'success' => true,
            'message' => 'Registration successful! Please login.',
            'user_id' => $user_id
        ]);
    } else {
        throw new Exception("Registration failed. Please try again.");
    }
    
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

