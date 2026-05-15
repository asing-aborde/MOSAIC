-- AdNU Mosaic Database Schema
-- Creates tables for pins, users (admin), and locations

CREATE DATABASE IF NOT EXISTS adnu_mosaic;
USE adnu_mosaic;

-- Users table (for admin authentication)
CREATE TABLE IF NOT EXISTS users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(120) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(100) NOT NULL,
  role ENUM('admin', 'moderator') DEFAULT 'admin',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Locations table (campus locations)
CREATE TABLE IF NOT EXISTS locations (
  location_id INT AUTO_INCREMENT PRIMARY KEY,
  location_name VARCHAR(100) NOT NULL,
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pins table (memory posts)
CREATE TABLE IF NOT EXISTS pins (
  pin_id INT AUTO_INCREMENT PRIMARY KEY,
  author VARCHAR(100),
  title VARCHAR(255) NOT NULL,
  content LONGTEXT NOT NULL,
  location_id INT,
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  location_name VARCHAR(100),
  category VARCHAR(50) DEFAULT 'campus',
  visibility ENUM('public', 'private') DEFAULT 'public',
  image_url LONGTEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (location_id) REFERENCES locations(location_id) ON DELETE SET NULL,
  INDEX idx_location_id (location_id),
  INDEX idx_created_at (created_at),
  INDEX idx_visibility (visibility)
);

-- Create default campus locations
INSERT INTO locations (location_name, latitude, longitude, description) VALUES
('Ateneo de Naga Main Campus', 13.6208, 123.1846, 'Main administrative building'),
('Science Building', 13.6210, 123.1850, 'College of Science and Mathematics'),
('Engineering Block', 13.6205, 123.1848, 'College of Engineering'),
('Student Center', 13.6212, 123.1844, 'Central gathering space for students'),
('Library', 13.6209, 123.1847, 'Main library facility'),
('Athletic Field', 13.6215, 123.1842, 'Sports and recreation area'),
('Cafeteria', 13.6207, 123.1845, 'Main dining facility'),
('Dormitory', 13.6214, 123.1849, 'Student housing');

-- Insert sample admin user (password: admin123 hashed with bcrypt)
-- Note: Replace with actual bcrypt hash in production
INSERT INTO users (email, password_hash, full_name, role) VALUES
('admin@adnu.edu.ph', '$2b$12$abcdefghijklmnopqrstuvwxyz', 'System Administrator', 'admin');

-- Create sample pins
INSERT INTO pins (author, title, content, location_id, latitude, longitude, location_name, category, visibility) VALUES
('Maria Santos', 'First Day Jitters', 'I still remember walking through the main gate on my first day. The campus was so quiet that early in the morning.', 1, 13.6208, 123.1846, 'Main Campus', 'campus', 'public'),
('Juan Dela Cruz', 'Midnight Study Sessions', 'The library became my second home during exam weeks. Coffee and textbooks - the student life!', 5, 13.6209, 123.1847, 'Library', 'campus', 'public'),
('Ana Gonzales', 'Championship Victory', 'Unforgettable moment when our team won the inter-college championship on this field!', 6, 13.6215, 123.1842, 'Athletic Field', 'campus', 'public');
