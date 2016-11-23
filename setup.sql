-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 23, 2016 at 02:40 PM
-- Server version: 5.7.16
-- PHP Version: 5.5.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `caParis`
--

-- --------------------------------------------------------

--
-- Table structure for table `releve`
--

CREATE TABLE `releve` (
  `id` int(12) UNSIGNED NOT NULL,
  `date` date NOT NULL,
  `dateValeur` date NOT NULL,
  `libelle` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `debitEuros` double DEFAULT NULL,
  `creditEuros` double DEFAULT NULL,
  `sha224Hash` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `releve`
--
ALTER TABLE `releve`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sha224Hash` (`sha224Hash`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `releve`
--
ALTER TABLE `releve`
  MODIFY `id` int(12) UNSIGNED NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
