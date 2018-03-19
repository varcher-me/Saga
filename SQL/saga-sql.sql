/*
SQLyog  v12.2.6 (64 bit)
MySQL - 5.7.19-log : Database - saga
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`saga` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin */;

USE `saga`;

/*Table structure for table `filelist` */

DROP TABLE IF EXISTS `filelist`;

CREATE TABLE `filelist` (
  `filename_server` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  `filename_secure` varchar(200) COLLATE utf8mb4_bin DEFAULT NULL,
  `filename_ext` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL,
  `file_size` bigint(20) unsigned DEFAULT NULL,
  `file_sha` varchar(40) COLLATE utf8mb4_bin DEFAULT NULL,
  `file_md5` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`filename_server`),
  KEY `IK1` (`file_size`,`filename_ext`,`file_sha`,`file_md5`),
  KEY `IK2` (`filename_secure`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

/*Table structure for table `history` */

DROP TABLE IF EXISTS `history`;

CREATE TABLE `history` (
  `uuid` varchar(40) COLLATE utf8mb4_bin NOT NULL,
  `seq_no` int(5) NOT NULL,
  `process_status` tinyint(3) unsigned DEFAULT NULL,
  `appid` varchar(5) COLLATE utf8mb4_bin DEFAULT NULL,
  `userid` varchar(40) COLLATE utf8mb4_bin DEFAULT NULL,
  `userip` varchar(40) COLLATE utf8mb4_bin DEFAULT NULL,
  `time_post` datetime DEFAULT NULL,
  `time_process` datetime DEFAULT NULL,
  `filename_post` varchar(200) COLLATE utf8mb4_bin DEFAULT NULL,
  `filename_secure` varchar(200) COLLATE utf8mb4_bin DEFAULT NULL,
  `filename_server` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `process_phase` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `process_comment` varchar(500) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`uuid`,`seq_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

/*Table structure for table `postlist` */

DROP TABLE IF EXISTS `postlist`;

CREATE TABLE `postlist` (
  `uuid` varchar(40) COLLATE utf8mb4_bin NOT NULL,
  `appid` varchar(5) COLLATE utf8mb4_bin DEFAULT NULL,
  `userid` varchar(40) COLLATE utf8mb4_bin DEFAULT NULL,
  `userip` varchar(40) COLLATE utf8mb4_bin DEFAULT NULL,
  `time_post` datetime DEFAULT NULL,
  `process_status` tinyint(3) unsigned DEFAULT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
