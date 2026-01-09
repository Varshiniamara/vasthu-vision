-- Add Analysis Results Table (if not exists)

CREATE TABLE IF NOT EXISTS analysis_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    space_id INT,
    floor_plan_id INT,
    energy_flow_score INT,
    room_placement_score INT,
    directional_score INT,
    overall_score INT,
    recommendations TEXT,
    analysis_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (space_id) REFERENCES spaces(id) ON DELETE SET NULL,
    FOREIGN KEY (floor_plan_id) REFERENCES floor_plans(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

