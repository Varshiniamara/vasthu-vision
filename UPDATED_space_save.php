<?php
/**
 * SPACE SAVE - Works with your existing db_connect.php
 */

// Include your existing database connection
require_once 'db_connect.php';

header('Content-Type: application/json');
session_start();

// Check login
if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['success' => false, 'message' => 'Please login first']);
    exit;
}

// Only accept POST
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
    if (empty($data['plotSize']) || empty($data['roomType']) || 
        empty($data['orientation']) || empty($data['floorNumber'])) {
        throw new Exception("All space details are required");
    }
    
    // Validate rooms
    if (empty($data['rooms']) || !is_array($data['rooms'])) {
        throw new Exception("At least one room is required");
    }
    
    // Start transaction
    $conn->begin_transaction();
    
    try {
        // Insert space
        $stmt = $conn->prepare("
            INSERT INTO spaces (user_id, plot_size, room_type, orientation, floor_number)
            VALUES (?, ?, ?, ?, ?)
        ");
        
        $stmt->bind_param("isssi",
            $_SESSION['user_id'],
            $data['plotSize'],
            $data['roomType'],
            $data['orientation'],
            $data['floorNumber']
        );
        
        $stmt->execute();
        $space_id = $conn->insert_id;
        
        // Insert rooms
        $stmt = $conn->prepare("
            INSERT INTO rooms (space_id, room_name, room_zone)
            VALUES (?, ?, ?)
        ");
        
        foreach ($data['rooms'] as $room) {
            if (empty($room['name']) || empty($room['zone'])) {
                throw new Exception("Room name and zone required");
            }
            
            $stmt->bind_param("iss", $space_id, $room['name'], $room['zone']);
            $stmt->execute();
        }
        
        // Log activity
        $stmt = $conn->prepare("INSERT INTO activity_log (user_id, action, description, ip_address) VALUES (?, 'space_created', ?, ?)");
        $desc = "Created space with " . count($data['rooms']) . " rooms";
        $ip = $_SERVER['REMOTE_ADDR'];
        $stmt->bind_param("iss", $_SESSION['user_id'], $desc, $ip);
        $stmt->execute();
        
        // Commit
        $conn->commit();
        
        echo json_encode([
            'success' => true,
            'message' => 'Space saved successfully!',
            'space_id' => $space_id
        ]);
        
    } catch (Exception $e) {
        $conn->rollback();
        throw $e;
    }
    
} catch (Exception $e) {
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'message' => $e->getMessage()
    ]);
}
?>

