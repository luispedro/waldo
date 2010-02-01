-- phpMyAdmin SQL Dump
-- version 3.2.2.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jan 17, 2010 at 08:03 PM
-- Server version: 5.1.37
-- PHP Version: 5.2.10-2ubuntu6.4

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

CREATE DATABASE waldo;
USE waldo;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `msdatabases`
--

-- --------------------------------------------------------

--
-- Table structure for table `db_to_ensembl`
--

CREATE TABLE IF NOT EXISTS `db_to_ensembl` (
  `dbname` varchar(10) NOT NULL,
  `entry_id` varchar(30) NOT NULL,
  `ensembl_id` varchar(50) NOT NULL,
  PRIMARY KEY (`dbname`,`entry_id`),
  KEY `ensembl_id` (`ensembl_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `esldb`
--

CREATE TABLE IF NOT EXISTS `esldb` (
  `entryid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `esldbid` varchar(50) NOT NULL,
  `experimental_annot` varchar(100) DEFAULT NULL,
  `similarity_annot` varchar(100) DEFAULT NULL,
  `uniprot_fulltext_annot` varchar(200) DEFAULT NULL,
  `uniprot_entry_id` varchar(20) DEFAULT NULL,
  `uniprot_homologue_id` varchar(20) DEFAULT NULL,
  `prediction` float NOT NULL,
  `db_type` enum('mouse','human') NOT NULL,
  PRIMARY KEY (`entryid`),
  KEY `esldbid` (`esldbid`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=124290 ;

-- --------------------------------------------------------

--
-- Table structure for table `locate`
--

CREATE TABLE IF NOT EXISTS `locate` (
  `locateid` int(10) unsigned NOT NULL,
  `images` text,
  `coloc_images` text,
  `db_type` enum('mouse','human') NOT NULL,
  PRIMARY KEY (`locateid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `locate_citations`
--

CREATE TABLE IF NOT EXISTS `locate_citations` (
  `locate_id` int(11) NOT NULL,
  `citationid` int(11) NOT NULL AUTO_INCREMENT,
  `author` varchar(100) NOT NULL,
  `title` varchar(200) NOT NULL,
  `citation_type` varchar(100) NOT NULL,
  `source_id` int(11) NOT NULL,
  `source_name` varchar(50) NOT NULL,
  `accn` varchar(50) NOT NULL,
  PRIMARY KEY (`citationid`),
  KEY `locate_id` (`locate_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=8077 ;

-- --------------------------------------------------------

--
-- Table structure for table `locate_external_annot`
--

CREATE TABLE IF NOT EXISTS `locate_external_annot` (
  `locate_id` int(11) NOT NULL,
  `annotid` int(11) NOT NULL AUTO_INCREMENT,
  `source_id` int(11) NOT NULL,
  `source_name` varchar(50) NOT NULL,
  `accn` varchar(50) NOT NULL,
  PRIMARY KEY (`annotid`),
  KEY `locate_id` (`locate_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=400164 ;

-- --------------------------------------------------------

--
-- Table structure for table `locate_locations`
--

CREATE TABLE IF NOT EXISTS `locate_locations` (
  `locate_id` int(11) NOT NULL,
  `cite_id` int(11) DEFAULT NULL COMMENT 'If not null, this entry is a citation location',
  `annot_id` int(11) DEFAULT NULL COMMENT 'If not null, this entry is an external annotation location',
  `goid` varchar(10) NOT NULL,
  PRIMARY KEY (`locate_id`),
  KEY `cite_id` (`cite_id`,`annot_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `locate_scl_predictions`
--

CREATE TABLE IF NOT EXISTS `locate_scl_predictions` (
  `locate_id` int(11) NOT NULL,
  `predictid` int(11) NOT NULL AUTO_INCREMENT,
  `source_id` int(11) NOT NULL,
  `method` varchar(50) NOT NULL,
  `location` varchar(50) NOT NULL,
  `goid` varchar(20) NOT NULL,
  `confidence` float NOT NULL,
  PRIMARY KEY (`predictid`),
  KEY `locate_id` (`locate_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=634803 ;

-- --------------------------------------------------------
