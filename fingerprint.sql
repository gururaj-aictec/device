/*
SQLyog Ultimate
MySQL - 5.7.32-log : Database - fingerprint
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`fingerprint` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin */;

USE `fingerprint`;

/*Table structure for table `access_day` */

DROP TABLE IF EXISTS `access_day`;

CREATE TABLE `access_day` (
  `id` int(11) NOT NULL,
  `serial` varchar(12) COLLATE utf8mb4_bin DEFAULT NULL,
  `name` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL,
  `start_time1` varchar(20) COLLATE utf8mb4_bin NOT NULL,
  `end_time1` varchar(20) COLLATE utf8mb4_bin NOT NULL,
  `start_time2` varchar(20) COLLATE utf8mb4_bin NOT NULL,
  `end_time2` varchar(20) COLLATE utf8mb4_bin NOT NULL,
  `start_time3` varchar(20) COLLATE utf8mb4_bin NOT NULL,
  `end_time3` varchar(20) COLLATE utf8mb4_bin NOT NULL,
  `start_time4` varchar(20) COLLATE utf8mb4_bin NOT NULL,
  `end_time4` varchar(20) COLLATE utf8mb4_bin NOT NULL,
  `start_time5` varchar(20) COLLATE utf8mb4_bin NOT NULL,
  `end_time5` varchar(20) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

/*Data for the table `access_day` */

insert  into `access_day`(`id`,`serial`,`name`,`start_time1`,`end_time1`,`start_time2`,`end_time2`,`start_time3`,`end_time3`,`start_time4`,`end_time4`,`start_time5`,`end_time5`) values 
(1,'222','233','08:00','18:00','00:00','00:00','00:00','00:00','00:00','00:00','00:00','00:00'),
(2,'334','33','08:00','18:00','00:00','00:00','00:00','00:00','00:00','00:00','00:00','00:00'),
(5,'334','33','08:00','18:00','00:00','00:00','00:00','00:00','00:00','00:00','00:00','00:00');

/*Table structure for table `access_week` */

DROP TABLE IF EXISTS `access_week`;

CREATE TABLE `access_week` (
  `id` int(11) NOT NULL,
  `serial` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL,
  `name` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL,
  `monday` int(20) NOT NULL,
  `tuesday` int(20) NOT NULL,
  `wednesday` int(20) NOT NULL,
  `thursday` int(20) NOT NULL,
  `friday` int(20) NOT NULL,
  `saturday` int(20) NOT NULL,
  `sunday` int(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

/*Data for the table `access_week` */

insert  into `access_week`(`id`,`serial`,`name`,`monday`,`tuesday`,`wednesday`,`thursday`,`friday`,`saturday`,`sunday`) values 
(1,'','',1,1,1,1,1,1,1);

/*Table structure for table `device` */

DROP TABLE IF EXISTS `device`;

CREATE TABLE `device` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `serial_num` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  `status` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

/*Data for the table `device` */



/*Table structure for table `enrollinfo` */

DROP TABLE IF EXISTS `enrollinfo`;

CREATE TABLE `enrollinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `enroll_id` bigint(20) NOT NULL,
  `backupnum` int(11) DEFAULT NULL,
  `imagepath` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `signatures` mediumtext COLLATE utf8mb4_bin,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4926 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

/*Data for the table `enrollinfo` */



/*Table structure for table `machine_command` */

DROP TABLE IF EXISTS `machine_command`;

CREATE TABLE `machine_command` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `serial` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `content` mediumtext COLLATE utf8mb4_bin,
  `status` int(11) NOT NULL DEFAULT '0',
  `send_status` int(11) NOT NULL DEFAULT '0',
  `err_count` int(11) NOT NULL DEFAULT '0',
  `run_time` datetime DEFAULT NULL,
  `gmt_crate` datetime NOT NULL,
  `gmt_modified` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23188 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

/*Data for the table `machine_command` */


/*Table structure for table `person` */

DROP TABLE IF EXISTS `person`;

CREATE TABLE `person` (
  `id` bigint(12) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `roll_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5322611263 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

/*Data for the table `person` */



/*Table structure for table `records` */

DROP TABLE IF EXISTS `records`;

CREATE TABLE `records` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `enroll_id` bigint(20) NOT NULL,
  `records_time` datetime NOT NULL,
  `mode` int(11) NOT NULL,
  `intOut` int(11) NOT NULL,
  `event` int(11) NOT NULL,
  `device_serial_num` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `temperature` double DEFAULT NULL,
  `image` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

/*Data for the table `records` */



/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
