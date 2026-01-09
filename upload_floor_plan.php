<?php
/**
 * Floor Plan Upload
 * Handles floor plan file uploads
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

// Only accept POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

try {
    // Check if files were uploaded
    if (empty($_FILES['files'])) {
        throw new Exception("No files uploaded");
    }
    
    $uploaded_files = [];
    $db = Database::getInstance()->getConnection();
    
    // Process each file
    $files = $_FILES['files'];
    $file_count = is_array($files['name']) ? count($files['name']) : 1;
    
    for ($i = 0; $i < $file_count; $i++) {
        // Get file details
        $file_name = is_array($files['name']) ? $files['name'][$i] : $files['name'];
        $file_tmp = is_array($files['tmp_name']) ? $files['tmp_name'][$i] : $files['tmp_name'];
        $file_size = is_array($files['size']) ? $files['size'][$i] : $files['size'];
        $file_error = is_array($files['error']) ? $files['error'][$i] : $files['error'];
        $file_type = is_array($files['type']) ? $files['type'][$i] : $files['type'];
        
        // Check for upload errors
        if ($file_error !== UPLOAD_ERR_OK) {
            throw new Exception("File upload error for: $file_name");
        }
        
        // Validate file size
        if ($file_size > MAX_FILE_SIZE) {
            throw new Exception("File too large: $file_name (Max: 5MB)");
        }
        
        // Validate file type
        $finfo = finfo_open(FILEINFO_MIME_TYPE);
        $mime_type = finfo_file($finfo, $file_tmp);
        finfo_close($finfo);
        
        if (!in_array($mime_type, ALLOWED_FILE_TYPES)) {
            throw new Exception("Invalid file type for: $file_name");
        }
        
        // Generate unique filename
        $extension = pathinfo($file_name, PATHINFO_EXTENSION);
        $new_filename = uniqid() . '_' . time() . '.' . $extension;
        $destination = UPLOAD_DIR . $new_filename;
        
        // Move uploaded file
        if (!move_uploaded_file($file_tmp, $destination)) {
            throw new Exception("Failed to save file: $file_name");
        }
        
        // Save to database
        $stmt = $db->prepare("
            INSERT INTO floor_plans (user_id, file_name, file_path, file_type, file_size)
            VALUES (?, ?, ?, ?, ?)
        ");
        
        $stmt->execute([
            $_SESSION['user_id'],
            $file_name,
            $new_filename,
            $mime_type,
            $file_size
        ]);
        
        $file_id = $db->lastInsertId();
        
        $uploaded_files[] = [
            'id' => $file_id,
            'name' => $file_name,
            'size' => $file_size,
            'type' => $mime_type,
            'url' => SITE_URL . '/uploads/' . $new_filename
        ];
    }
    
    // Log activity
    $stmt = $db->prepare("
        INSERT INTO activity_log (user_id, action, description, ip_address)
        VALUES (?, 'floor_plan_upload', ?, ?)
    ");
    $stmt->execute([
        $_SESSION['user_id'],
        "Uploaded " . count($uploaded_files) . " floor plan(s)",
        $_SERVER['REMOTE_ADDR']
    ]);
    
    echo json_encode([
        'success' => true,
        'message' => 'Files uploaded successfully!',
        'files' => $uploaded_files
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

