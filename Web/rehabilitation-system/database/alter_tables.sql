-- ============================================
-- File: alter_tables.sql
-- Description: Add all new modifications to the database
-- ============================================

USE rehabilitation_system;

-- ============================================
-- 1. Add all new columns to patients table
-- ============================================

-- Add photo_url column
ALTER TABLE patients 
ADD COLUMN photo_url VARCHAR(255) DEFAULT NULL AFTER external_rotation;

-- Add affected_hand column (if error 1060, it's already exists - continue)
ALTER TABLE patients 
ADD COLUMN affected_hand ENUM('left','right','both') DEFAULT 'right' AFTER gender;

-- Add video_url column
ALTER TABLE patients 
ADD COLUMN video_url VARCHAR(255) DEFAULT NULL AFTER photo_url;

-- Add assessment dates
ALTER TABLE patients 
ADD COLUMN initial_assessment_date TIMESTAMP NULL AFTER video_url,
ADD COLUMN last_assessment_date TIMESTAMP NULL AFTER initial_assessment_date;

-- ============================================
-- 2. Create progress_tracking table
-- ============================================
CREATE TABLE IF NOT EXISTS progress_tracking (
  `id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `tracking_date` date NOT NULL,
  `shoulder_strength` int DEFAULT '0',
  `elbow_strength` int DEFAULT '0',
  `wrist_strength` int DEFAULT '0',
  `grip_strength` int DEFAULT '0',
  `external_rotation` int DEFAULT '0',
  `notes` text,
  `recorded_by` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  KEY `tracking_date` (`tracking_date`),
  CONSTRAINT `progress_tracking_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================
-- 3. Verify new columns
-- ============================================
SELECT '=== New columns in patients table ===' as '';
DESCRIBE patients;

-- ============================================
-- 4. Verify new table
-- ============================================
SELECT '=== Existing tables ===' as '';
SHOW TABLES LIKE 'progress_tracking';

-- ============================================
-- Success message
-- ============================================
SELECT '✅ All modifications added successfully' as 'Result';