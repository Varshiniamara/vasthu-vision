<?php
/**
 * Get User Data API
 * Returns user information and their spaces
 */

require_once 'config.php';
require_once 'Database.php';

header('Content-Type: application/json');

// Check if user is logged in
if (!isset($_SESSION['user_id'])) {
    http_response_code(401);
    echo json_encode(['success' => false, 'message' => 'Please login first']);
    exit;
}

try {
    $db = Database::getInstance()->getConnection();
    
    // Get user data
    $stmt = $db->prepare("
        SELECT id, first_name, last_name, email, phone, gender, date_of_birth, created_at, last_login
        FROM users
        WHERE id = ?
    ");
    $stmt->execute([$_SESSION['user_id']]);
    $user = $stmt->fetch();
    
    if (!$user) {
        throw new Exception("User not found");
    }
    
    // Get user's spaces
    $stmt = $db->prepare("
        SELECT s.*, COUNT(r.id) as room_count
        FROM spaces s
        LEFT JOIN rooms r ON s.id = r.space_id
        WHERE s.user_id = ?
        GROUP BY s.id
        ORDER BY s.created_at DESC
    ");
    $stmt->execute([$_SESSION['user_id']]);
    $spaces = $stmt->fetchAll();
    
    // Get rooms for each space
    foreach ($spaces as &$space) {
        $stmt = $db->prepare("
            SELECT id, room_name, room_zone
            FROM rooms
            WHERE space_id = ?
        ");
        $stmt->execute([$space['id']]);
        $space['rooms'] = $stmt->fetchAll();
    }
    
    // Get user's floor plans
    $stmt = $db->prepare("
        SELECT id, file_name, file_path, file_type, file_size, uploaded_at
        FROM floor_plans
        WHERE user_id = ?
        ORDER BY uploaded_at DESC
        LIMIT 10
    ");
    $stmt->execute([$_SESSION['user_id']]);
    $floor_plans = $stmt->fetchAll();
    
    // Get analysis results
    $stmt = $db->prepare("
        SELECT id, overall_score, energy_flow_score, room_placement_score, directional_score, created_at
        FROM analysis_results
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 5
    ");
    $stmt->execute([$_SESSION['user_id']]);
    $analyses = $stmt->fetchAll();
    
    echo json_encode([
        'success' => true,
        'user' => $user,
        'spaces' => $spaces,
        'floor_plans' => $floor_plans,
        'analyses' => $analyses
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

