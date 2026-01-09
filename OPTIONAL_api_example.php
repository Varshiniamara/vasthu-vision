<?php
/**
 * EXAMPLE API ENDPOINT WITH TOKEN AUTHENTICATION
 * Shows how to use token verification in your APIs
 */

require_once 'OPTIONAL_verify_token.php';

header('Content-Type: application/json');

// Verify API token (this will exit if invalid)
$user = verifyApiToken();

// If we reach here, user is authenticated
try {
    // Your API logic here
    // Example: Get user's spaces
    
    $stmt = $conn->prepare("
        SELECT s.*, COUNT(r.id) as room_count
        FROM spaces s
        LEFT JOIN rooms r ON s.id = r.space_id
        WHERE s.user_id = ?
        GROUP BY s.id
        ORDER BY s.created_at DESC
    ");
    $stmt->bind_param("i", $user['id']);
    $stmt->execute();
    $result = $stmt->get_result();
    $spaces = $result->fetch_all(MYSQLI_ASSOC);
    
    echo json_encode([
        'success' => true,
        'user' => [
            'id' => $user['id'],
            'name' => $user['first_name'] . ' ' . $user['last_name'],
            'email' => $user['email']
        ],
        'spaces' => $spaces
    ]);
    
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Server error: ' . $e->getMessage()
    ]);
}
?>

