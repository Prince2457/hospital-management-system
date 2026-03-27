-- HMS database Schema 
-- Prince Nkansah | 2026

CREATE DATABASE IF NOT EXISTS hospital_db;
USE hospital_db;

--Users table
CREATE TABLE `users` (
    `user_id` int NOT NULL AUTO_INCREMENT,
    `username` varchar(50) NOT NULL,
    `password_hash` varchar(255) NOT NULL,
    `role` enum('admin','medical_superintendent','hospital_administrator','doctor','nurse','lab_technician','cashier','accountant','auditor','pharmacist','record_manager','storekeeper','procurement_officer') NOT NULL,
    `full_name` varchar(100) NOT NULL,
    `email` varchar(100) DEFAULT NULL,
    `phone` varchar(20) DEFAULT NULL,
    `is_active` tinyint(1) NOT NULL DEFAULT '1',
    `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    `last_login` timestamp NULL DEFAULT NULL,
    PRIMARY KEY (`user_id`),
    UNIQUE KEY `username` (`username`),
    UNIQUE KEY `email` (`email`)
)   ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Patients table
CREATE TABLE `patients` (
    `patient_id` int NOT NULL AUTO_INCREMENT,
    `full_name` varchar(100) NOT NULL,
    `ghana_card_number` varchar(20) NOT NULL,
    `date_of_birth` date NOT NULL,
    `gender` enum('male','female','other') NOT NULL,
    `phone` varchar(20) NOT NULL,
    `email` varchar(100) DEFAULT NULL,
    `address` text NOT NULL,
    `region` varchar(50) NOT NULL,
    `blood_group` varchar(5) DEFAULT NULL,
    `nhis_number` varchar(20) DEFAULT NULL,
    `nhis_expiry` date DEFAULT NULL,
    `emergency_contact_name` varchar(100) NOT NULL,
    `emergency_contact_phone` varchar(20) NOT NULL,
    `registered_by` int NOT NULL,
    `registered_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`patient_id`),
    UNIQUE KEY `ghana_card_number` (`ghana_card_number`),
    KEY `registered_by` (`registered_by`),
    KEY `idx_patients_full_name` (`full_name`),
    KEY `idx_patients_phone` (`phone`),
    CONSTRAINT `patients_ibfk_1` FOREIGN KEY (`registered_by`) REFERENCES `users` (`user_id`)
)   ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Doctors table
CREATE TABLE `doctors` (
    `doctor_id` int NOT NULL AUTO_INCREMENT,
    `user_id` int NOT NULL,
    `specialization` varchar(100) NOT NULL,
    `qualification` varchar(200) NOT NULL,
    `license_number` varchar(50) NOT NULL,
    `department` varchar(100) NOT NULL,
    `available_days` varchar(100) DEFAULT NULL,
    `consultation_fee` decimal(10,2) NOT NULL,
    PRIMARY KEY (`doctor_id`),
    UNIQUE KEY `license_number` (`license_number`),
    KEY `user_id` (`user_id`),
    CONSTRAINT `doctors_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
)   ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 

-- Appointments table
CREATE TABLE `appointments` (
    `appointment_id` int NOT NULL AUTO_INCREMENT,
    `patient_id` int NOT NULL,
    `doctor_id` int NOT NULL,
    `appointment_date` date NOT NULL,
    `appointment_time` time NOT NULL,
    `status` enum('scheduled','completed','cancelled') DEFAULT 'scheduled',
    `notes` text,
    `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`appointment_id`),
    KEY `patient_id` (`patient_id`),
    KEY `doctor_id` (`doctor_id`),
    KEY `idx_appointments_date` (`appointment_date`),
    CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE CASCADE,
    CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`) ON DELETE CASCADE
)   ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Billing table
CREATE TABLE `billing` (
    `bill_id` int NOT NULL AUTO_INCREMENT,
    `patient_id` int NOT NULL,
    `appointment_id` int NOT NULL,
    `bill_item` varchar(255) NOT NULL,
    `amount` decimal(10,2) NOT NULL,
    `payment_status` enum('pending','paid','overdue') DEFAULT 'pending',
    `payment_date` date DEFAULT NULL,
    `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`bill_id`),
    KEY `patient_id` (`patient_id`),
    KEY `appointment_id` (`appointment_id`),
    KEY `idx_billing_status` (`payment_status`),
    CONSTRAINT `billing_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`),
    CONSTRAINT `billing_ibfk_2` FOREIGN KEY (`appointment_id`) REFERENCES `appointments` (`appointment_id`)
)   ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4;

-- Inventory table
CREATE TABLE `inventory` (
    `item_id` int NOT NULL AUTO_INCREMENT,
    `item_name` varchar(255) NOT NULL,
    `item_category` enum('medicine','equipment','supplies') NOT NULL,
    `quantity` int NOT NULL DEFAULT '0',
    `reorder_level` int NOT NULL,
    `item_cost` decimal(10,2) NOT NULL,
    `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`item_id`)
)   ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 

-- Medical Records table
CREATE TABLE `medical_records` (
    `record_id` int NOT NULL AUTO_INCREMENT,
    `patient_id` int NOT NULL,
    `doctor_id` int NOT NULL,
    `appointment_id` int NOT NULL,
    `diagnosis` text NOT NULL,
    `treatment` text,
    `lab_tests` text,
    `notes` text,
    `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`record_id`),
    KEY `patient_id` (`patient_id`),
    KEY `doctor_id` (`doctor_id`),
    KEY `appointment_id` (`appointment_id`),
    CONSTRAINT `medical_records_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE CASCADE,
    CONSTRAINT `medical_records_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`) ON DELETE CASCADE,
    CONSTRAINT `medical_records_ibfk_3` FOREIGN KEY (`appointment_id`) REFERENCES `appointments` (`appointment_id`) ON DELETE CASCADE
)   ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;