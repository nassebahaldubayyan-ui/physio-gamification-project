-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: rehabilitation_system
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Create database
--
DROP DATABASE IF EXISTS `rehabilitation_system`;
CREATE DATABASE `rehabilitation_system`;
USE `rehabilitation_system`;

-- ============================================
-- Table: users
-- ============================================
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('patient','doctor') NOT NULL,
  `phone` varchar(20) NOT NULL,
  `avatar` varchar(255) DEFAULT 'default-avatar.png',
  `is_active` tinyint(1) DEFAULT '1',
  `last_login` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================
-- Table: patients (with all new columns)
-- ============================================
DROP TABLE IF EXISTS `patients`;
CREATE TABLE `patients` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `patient_id` varchar(20) NOT NULL,
  `date_of_birth` date NOT NULL,
  `gender` enum('male','female','other') NOT NULL,
  `affected_hand` enum('left','right','both') DEFAULT 'right',
  `medical_condition` varchar(100) NOT NULL,
  `therapy_type` varchar(100) NOT NULL,
  `current_level` int DEFAULT '1',
  `assigned_doctor_id` int DEFAULT NULL,
  `emergency_contact_name` varchar(100) DEFAULT NULL,
  `emergency_contact_phone` varchar(20) DEFAULT NULL,
  `address` text,
  `city` varchar(100) DEFAULT NULL,
  `country` varchar(100) DEFAULT 'Saudi Arabia',
  `shoulder_strength` int DEFAULT '0',
  `elbow_strength` int DEFAULT '0',
  `wrist_strength` int DEFAULT '0',
  `grip_strength` int DEFAULT '0',
  `external_rotation` int DEFAULT '0',
  `photo_url` varchar(255) DEFAULT NULL,
  `video_url` varchar(255) DEFAULT NULL,
  `initial_assessment_date` timestamp NULL DEFAULT NULL,
  `last_assessment_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `patient_id` (`patient_id`),
  CONSTRAINT `patients_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================
-- Table: doctors
-- ============================================
DROP TABLE IF EXISTS `doctors`;
CREATE TABLE `doctors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `doctor_id` varchar(20) NOT NULL,
  `specialty` varchar(100) NOT NULL,
  `license_number` varchar(50) NOT NULL,
  `hospital` varchar(200) NOT NULL,
  `experience` int DEFAULT '0',
  `available` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `doctor_id` (`doctor_id`),
  UNIQUE KEY `license_number` (`license_number`),
  CONSTRAINT `doctors_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================
-- Table: messages
-- ============================================
DROP TABLE IF EXISTS `messages`;
CREATE TABLE `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sender_id` int NOT NULL,
  `receiver_id` int NOT NULL,
  `message` text NOT NULL,
  `is_read` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `sender_id` (`sender_id`),
  KEY `receiver_id` (`receiver_id`),
  CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`),
  CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================
-- Table: game_sessions
-- ============================================
DROP TABLE IF EXISTS `game_sessions`;
CREATE TABLE `game_sessions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `game_type` enum('catching-stars','matching-game','catching-objects') NOT NULL,
  `level` int NOT NULL,
  `score` int NOT NULL,
  `duration` int NOT NULL,
  `accuracy` int DEFAULT NULL,
  `stars_caught` int DEFAULT '0',
  `matches_made` int DEFAULT '0',
  `objects_caught` int DEFAULT '0',
  `shoulder_activation` int DEFAULT '0',
  `elbow_activation` int DEFAULT '0',
  `wrist_activation` int DEFAULT '0',
  `grip_activation` int DEFAULT '0',
  `external_rotation` int DEFAULT '0',
  `shoulder_shrug` tinyint(1) DEFAULT '0',
  `completed` tinyint(1) DEFAULT '1',
  `session_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `game_sessions_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================
-- Table: progress_tracking (NEW - for storing daily/weekly progress)
-- ============================================
DROP TABLE IF EXISTS `progress_tracking`;
CREATE TABLE `progress_tracking` (
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
-- Insert sample data
-- ============================================

-- Insert patients into users table (passwords are hashed: '123456')
INSERT INTO users (name, email, password, role, phone) VALUES
('Ali Ahmed', 'ali@rehab.com', '$2a$10$NkM3QqZkXmYxLqRqLqRqLuQqRqLqRqLqRqLqRqLqRqLqRqLqRqLq', 'patient', '0501111111'),
('Sara Khaled', 'sara@rehab.com', '$2a$10$NkM3QqZkXmYxLqRqLqRqLuQqRqLqRqLqRqLqRqLqRqLqRqLqRqLq', 'patient', '0502222222'),
('Omar Hassan', 'omar@rehab.com', '$2a$10$NkM3QqZkXmYxLqRqLqRqLuQqRqLqRqLqRqLqRqLqRqLqRqLqRqLq', 'patient', '0503333333');

-- Insert patients data with new fields
INSERT INTO patients (user_id, patient_id, date_of_birth, gender, affected_hand, medical_condition, therapy_type, current_level, shoulder_strength, elbow_strength, wrist_strength, grip_strength, external_rotation) VALUES
(1, 'PT001', '2018-01-15', 'male', 'right', 'Motor Disability', 'Physical Therapy', 4, 85, 78, 82, 79, 92),
(2, 'PT002', '2019-03-20', 'female', 'left', 'Arm Weakness', 'Occupational Therapy', 3, 92, 88, 86, 89, 88),
(3, 'PT003', '2017-11-05', 'male', 'both', 'Movement Disorder', 'Developmental Therapy', 5, 88, 85, 90, 85, 96);

-- Insert doctors into users table
INSERT INTO users (name, email, password, role, phone) VALUES
('Dr. Ahmad', 'dr.ahmad@clinic.com', '$2a$10$NkM3QqZkXmYxLqRqLqRqLuQqRqLqRqLqRqLqRqLqRqLqRqLqRqLq', 'doctor', '0500000000'),
('Dr. Sarah', 'dr.sarah@clinic.com', '$2a$10$NkM3QqZkXmYxLqRqLqRqLuQqRqLqRqLqRqLqRqLqRqLqRqLqRqLq', 'doctor', '0501111111');

-- Insert doctors data
INSERT INTO doctors (user_id, doctor_id, specialty, license_number, hospital, experience) VALUES
(4, 'DR001', 'Physiotherapy', 'LIC001', 'Central Hospital', 10),
(5, 'DR002', 'Occupational Therapy', 'LIC002', 'Rehabilitation Center', 8);

-- Insert sample progress tracking data
INSERT INTO progress_tracking (patient_id, tracking_date, shoulder_strength, elbow_strength, wrist_strength, grip_strength, external_rotation) VALUES
(1, DATE_SUB(CURDATE(), INTERVAL 6 DAY), 80, 73, 76, 74, 85),
(1, DATE_SUB(CURDATE(), INTERVAL 5 DAY), 81, 74, 77, 75, 86),
(1, DATE_SUB(CURDATE(), INTERVAL 4 DAY), 82, 75, 78, 76, 88),
(1, DATE_SUB(CURDATE(), INTERVAL 3 DAY), 83, 76, 79, 77, 89),
(1, DATE_SUB(CURDATE(), INTERVAL 2 DAY), 84, 77, 80, 78, 90),
(1, DATE_SUB(CURDATE(), INTERVAL 1 DAY), 85, 78, 81, 79, 91),
(1, CURDATE(), 85, 78, 82, 79, 92);

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed