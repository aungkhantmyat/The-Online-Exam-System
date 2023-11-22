-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 22, 2023 at 05:48 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `examproctordb`
--

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `ID` int(125) NOT NULL,
  `Name` varchar(65) NOT NULL,
  `Email` varchar(85) NOT NULL,
  `Password` varchar(85) NOT NULL,
  `Role` varchar(65) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`ID`, `Name`, `Email`, `Password`, `Role`) VALUES
(1, 'Aung Khant Myat', 'akm@gmail.com', 'akm', 'STUDENT'),
(2, 'Admin 1', 'admin1@gmail.com', 'admin1@2023', 'ADMIN'),
(4, 'Tun Ye Min', 'tym@gmail.com', 'tym', 'STUDENT'),
(5, 'Khin Nyo Nyo Theint', 'knnt@gmail.com', 'knnt', 'STUDENT'),
(6, 'Chu Khin Khin', 'ckk@gmail.com', 'ckk', 'STUDENT'),
(7, 'Naw Si Si', 'nss@gmail.com', 'nss', 'STUDENT'),
(8, 'Myat Thiri Khant', 'mtk@gmail.com', 'mtk', 'STUDENT'),
(9, 'Youn Thinzar', 'ytz@gmail.com', 'ytz', 'STUDENT'),
(10, 'Ye Thu Aung', 'yta@gmailcom', 'yta', 'STUDENT');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `ID` int(125) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
