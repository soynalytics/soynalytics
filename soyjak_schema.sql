SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

DROP DATABASE soyjak;
CREATE DATABASE soyjak;
USE soyjak;

CREATE USER IF NOT EXISTS 'soyscraper_user'@'%' IDENTIFIED BY 'PUTURPASSWORDHERE';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, FILE, INDEX, ALTER ON *.* TO 'soyscraper_user'@'%';
FLUSH PRIVILEGES;
-- !!!change password above!!!

CREATE TABLE `descriptions` (
  `board` text NOT NULL,
  `title` text NOT NULL,
  `description` text NOT NULL,
  `time` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `news` (
  `link` text NOT NULL COMMENT 'news post link',
  `added` text NOT NULL COMMENT 'news post date added',
  `title` text NOT NULL COMMENT 'news post title',
  `time` int(11) NOT NULL COMMENT 'unix timestamp of scrape'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `pph` (
  `board` text NOT NULL COMMENT 'board link',
  `pph` int(11) NOT NULL COMMENT 'posts per hour',
  `posters` int(11) NOT NULL COMMENT 'number of posters',
  `count` int(11) NOT NULL COMMENT 'total number of posts',
  `time` int(11) NOT NULL COMMENT 'unix timestamp of scrape'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `rtl` (
  `score` float NOT NULL COMMENT 'average score',
  `voters` int(11) NOT NULL COMMENT 'number of voters ',
  `time` int(11) NOT NULL COMMENT ' unix timestamp of scrape '
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `statistics` (
  `posts` int(11) NOT NULL COMMENT 'number of posts',
  `posters` int(11) NOT NULL COMMENT 'number of posters',
  `content` float NOT NULL COMMENT 'content in gigabytes',
  `time` int(11) NOT NULL COMMENT ' unix timestamp of scrape '
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

ALTER TABLE `news`
  ADD UNIQUE KEY `link` (`link`) USING HASH;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
