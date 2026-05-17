-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 14, 2026 at 08:18 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `adnu_mosaic`
--

-- --------------------------------------------------------

--
-- Table structure for table `locations`
--

CREATE TABLE `locations` (
  `location_id` int(11) NOT NULL,
  `location_name` varchar(100) NOT NULL,
  `latitude` decimal(10,8) DEFAULT NULL,
  `longitude` decimal(11,8) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `locations`
--

INSERT INTO `locations` (`location_id`, `location_name`, `latitude`, `longitude`, `description`, `created_at`) VALUES
(9, 'Xavier Grounds', 13.63008277, 123.18519911, NULL, '2026-05-14 17:27:18'),
(10, 'Xavier Hall', 13.62972826, 123.18505964, NULL, '2026-05-14 17:27:18'),
(11, 'Gymnasium', 13.62953015, 123.18491614, NULL, '2026-05-14 17:27:18'),
(12, 'Church of Christ the King', 13.63084298, 123.18555984, NULL, '2026-05-14 17:27:18'),
(13, 'Faber Center', 13.63102601, 123.18585982, NULL, '2026-05-14 17:27:18'),
(14, 'Ignatius House', 13.63125287, 123.18573351, NULL, '2026-05-14 17:27:18'),
(15, 'Phelan Hall', 13.62999748, 123.18434707, NULL, '2026-05-14 17:27:18'),
(16, 'Dolan Building', 13.63024392, 123.18445712, NULL, '2026-05-14 17:27:18'),
(17, 'Four Pillars', 13.63043611, 123.18508549, NULL, '2026-05-14 17:27:18'),
(18, 'Administration Building', 13.63038807, 123.18488454, NULL, '2026-05-14 17:27:18'),
(19, 'Burns Building', 13.63099719, 123.18485902, NULL, '2026-05-14 17:27:18'),
(20, 'Coko Cafe', 13.63104524, 123.18522584, NULL, '2026-05-14 17:27:18'),
(21, 'Entrepreneurship Building', 13.63137692, 123.18488773, NULL, '2026-05-14 17:27:18'),
(22, 'Tennis Court', 13.63147049, 123.18469865, NULL, '2026-05-14 17:27:18'),
(23, 'Bonoan Hall', 13.63123814, 123.18437612, NULL, '2026-05-14 17:27:18'),
(24, 'Alingal Building', 13.63169187, 123.18431748, NULL, '2026-05-14 17:27:18'),
(25, 'Soccer Field', 13.63208861, 123.18437612, NULL, '2026-05-14 17:27:18'),
(26, 'Covered Court', 13.63209957, 123.18497382, NULL, '2026-05-14 17:27:18'),
(27, 'Richie Fernando Hall', 13.63133714, 123.18410309, NULL, '2026-05-14 17:27:18'),
(28, 'James O\'Brien Library', 13.63098220, 123.18391171, NULL, '2026-05-14 17:27:18'),
(29, 'Arrupe Building', 13.63146733, 123.18381123, NULL, '2026-05-14 17:27:18'),
(30, 'Adriatico Building', 13.63049242, 123.18382559, NULL, '2026-05-14 17:27:18'),
(31, 'Engineer Building', 13.62972270, 123.18364733, NULL, '2026-05-14 17:27:18'),
(32, 'Belardo/SHS Building', 13.62966926, 123.18399468, NULL, '2026-05-14 17:27:18'),
(33, 'Ignatius Park', 13.63069479, 123.18455132, NULL, '2026-05-14 17:27:18'),
(34, 'Madrigal Hall', 13.63113385, 123.18514615, NULL, '2026-05-14 17:27:18'),
(35, 'Santos Building', 13.63020094, 123.18456147, NULL, '2026-05-14 17:27:18');

-- --------------------------------------------------------

--
-- Table structure for table `pins`
--

CREATE TABLE `pins` (
  `pin_id` int(11) NOT NULL,
  `author` varchar(100) DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  `content` longtext NOT NULL,
  `location_id` int(11) DEFAULT NULL,
  `latitude` decimal(10,8) DEFAULT NULL,
  `longitude` decimal(11,8) DEFAULT NULL,
  `location_name` varchar(100) DEFAULT NULL,
  `category` varchar(50) DEFAULT 'campus',
  `visibility` enum('public','private') DEFAULT 'public',
  `image_url` varchar(500) DEFAULT NULL,
  `media_type` enum('image','video') DEFAULT 'image',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pins`
--

INSERT INTO `pins` (`pin_id`, `author`, `title`, `content`, `location_id`, `latitude`, `longitude`, `location_name`, `category`, `visibility`, `image_url`, `created_at`, `updated_at`) VALUES
(1, 'Maria Santos', 'First Day Jitters', 'I still remember walking through the main gate on my first day. The campus was so quiet that early in the morning.', NULL, 13.62080000, 123.18460000, 'Main Campus', 'campus', 'public', NULL, '2026-05-14 16:59:09', '2026-05-14 16:59:09'),
(2, 'Juan Dela Cruz', 'Midnight Study Sessions', 'The library became my second home during exam weeks. Coffee and textbooks - the student life!', NULL, 13.62090000, 123.18470000, 'Library', 'campus', 'public', NULL, '2026-05-14 16:59:09', '2026-05-14 16:59:09'),
(3, 'Ana Gonzales', 'Championship Victory', 'Unforgettable moment when our team won the inter-college championship on this field!', NULL, 13.62150000, 123.18420000, 'Athletic Field', 'campus', 'public', NULL, '2026-05-14 16:59:09', '2026-05-14 16:59:09'),
(4, 'asing', 'vibe igdi guysss', 'masiramon ang manok sa bambamsss', 23, 13.63123814, 123.18437612, 'Bonoan Hall', 'campus', 'public', NULL, '2026-05-14 17:29:59', '2026-05-14 17:29:59'),
(5, 'mat', 'maluwagon ako guysss', 'plssssss', 23, 13.63123814, 123.18437612, 'Bonoan Hall', 'campus', 'public', NULL, '2026-05-14 17:30:34', '2026-05-14 17:30:34'),
(6, 'matthew', 'maluwagon na ako igdi guysssss', 'irigdi na kamoooooo', 26, 13.63209957, 123.18497382, 'Covered Court', 'campus', 'public', NULL, '2026-05-14 17:33:10', '2026-05-14 17:33:10'),
(7, 'kuku', 'i love shenen', 'karaduan na', 33, 13.63069479, 123.18455132, 'Ignatius Park', 'campus', 'public', NULL, '2026-05-14 17:41:38', '2026-05-14 17:41:38'),
(8, 'shean', 'shean', 'shean', 11, 13.62953015, 123.18491614, 'Gymnasium', 'campus', 'public', NULL, '2026-05-14 17:44:21', '2026-05-14 17:44:21'),
(9, 'niku', 'NAWAWARA CP KOOOOO', 'taka kuku tas asingggg', 26, 13.63209957, 123.18497382, 'Covered Court', 'campus', 'public', NULL, '2026-05-14 17:45:20', '2026-05-14 17:45:20');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `role` enum('admin','moderator') DEFAULT 'admin',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `email`, `password_hash`, `full_name`, `role`, `created_at`, `updated_at`) VALUES
(1, 'admin@adnu.edu.ph', '$2b$12$abcdefghijklmnopqrstuvwxyz', 'System Administrator', 'admin', '2026-05-14 16:59:09', '2026-05-14 16:59:09');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `locations`
--
ALTER TABLE `locations`
  ADD PRIMARY KEY (`location_id`);

--
-- Indexes for table `pins`
--
ALTER TABLE `pins`
  ADD PRIMARY KEY (`pin_id`),
  ADD KEY `idx_location_id` (`location_id`),
  ADD KEY `idx_created_at` (`created_at`),
  ADD KEY `idx_visibility` (`visibility`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `locations`
--
ALTER TABLE `locations`
  MODIFY `location_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `pins`
--
ALTER TABLE `pins`
  MODIFY `pin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `pins`
--
ALTER TABLE `pins`
  ADD CONSTRAINT `pins_ibfk_1` FOREIGN KEY (`location_id`) REFERENCES `locations` (`location_id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
