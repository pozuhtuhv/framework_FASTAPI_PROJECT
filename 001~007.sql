-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.36 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.7.0.6850
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for fastapi_test
CREATE DATABASE IF NOT EXISTS `fastapi_test` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `fastapi_test`;

-- Dumping structure for table fastapi_test.posts
CREATE TABLE IF NOT EXISTS `posts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(50) DEFAULT NULL,
  `description` varchar(300) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `post_time` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_posts_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table fastapi_test.posts: ~17 rows (approximately)
INSERT INTO `posts` (`id`, `title`, `description`, `username`, `post_time`) VALUES
	(1, '14224', '142421', 'asdf', '2024-05-12 22:05'),
	(5, '앗뇽', '하위', 'aaaa', '2024-05-12 23:37'),
	(6, '14214', '42142', 'aaaa', '2024-05-12 23:39'),
	(7, '횬소기', '짱짱맨', 'aaaa', '2024-05-12 23:42'),
	(8, 'wqrwrq', 'rwqrwqfwfwq', 'aaaa', '2024-05-13 11:24'),
	(9, 'fasfsa', 'gsdsg', 'aaaa', '2024-05-13 11:38'),
	(10, 'wqfqfqwf', 'ㅈㄼㅂㅈㄹ', 'aaaa', '2024-05-13 11:40'),
	(11, 'fwqwfq', 'wfqfwq', 'aaaa', '2024-05-13 11:40'),
	(12, 'ㅁㄹㄴㄴㅁㄹ', 'ㅁㄹㄴㄹㅁㄴㄻㄴㄹ', 'aaaa', '2024-05-13 11:43'),
	(13, 'ㅂㅈㄹㄹㅈㅂ', 'ㄹㅈㅂㄹㅈㅂ', 'aaaa', '2024-05-13 11:44'),
	(14, 'ㅁㄴㄻㄴㄹ', 'ㅁㄴㄻㄴㄹ', 'aaaa', '2024-05-13 11:46'),
	(15, 'ㅂㅈㄹㄼㅈ', 'ㄼㅈㄹ', 'aaaa', '2024-05-13 11:48'),
	(16, 'ㅈㅂㄹ', 'ㅈㄼㄹㅈㅂ', 'aaaa', '2024-05-13 11:48'),
	(17, 'ㅁㄹㄴㅁㄹㄴ', 'ㅈㅂㄼㅈㅎㅂㅈ', 'aaaa', '2024-05-13 11:53'),
	(18, 'ㅁㄴㄹㄻㄴ', '21ㄱ2121ㅁㄴㅇㅎㅁㄴㄱ1', 'aaaa', '2024-05-13 11:54'),
	(19, 'fqwfwq', 'fqwfqw', 'aaaa', '2024-05-13 18:06'),
	(20, '1421', '124412', 'aaaa', '2024-05-13 18:11');

-- Dumping structure for table fastapi_test.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(50) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `role` varchar(20) DEFAULT NULL,
  `hashed_password` varchar(128) DEFAULT NULL,
  `auth_time` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_username` (`username`),
  UNIQUE KEY `ix_users_email` (`email`),
  KEY `ix_users_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table fastapi_test.users: ~2 rows (approximately)
INSERT INTO `users` (`id`, `email`, `username`, `role`, `hashed_password`, `auth_time`) VALUES
	(1, 'asdf@nave.rcom', 'asdf', 'nomal', '$2b$12$ok4CPPlBwO7eDq1Zok4sEelot0gMW6aXJaB11QB9io/xcvJVT0oXK', '2024-05-12 22:05'),
	(2, 'aaaa@aaa.com', 'aaaa', 'nomal', '$2b$12$nDr9r5fTE4LiWh4U73RyOuOw63VDgInppL1ya67j/FVQxv45fxHSS', '2024-05-12 22:14');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
