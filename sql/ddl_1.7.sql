-- 表 test_case
DROP TABLE IF EXISTS `test_case`;
CREATE TABLE `test_case` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` longtext NOT NULL,
  `comment` varchar(255) NOT NULL,
  `params` text,
  `rule_id` int(11) NOT NULL,
  `case_set_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `case_1c671d36` (`rule_id`),
  KEY `case_5d0eef6f` (`case_set_id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

-- 表 case_set
DROP TABLE IF EXISTS `case_set`;
CREATE TABLE `case_set` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `comment` varchar(255) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- 表 service_item
DROP TABLE IF EXISTS `service_item`;
CREATE TABLE `service_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idc` int(11) NOT NULL,
  `ip` varchar(32) NOT NULL,
  `port` int(11) NOT NULL,
  `is_use_proxy` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `service_item_425ae3c4` (`group_id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;

-- 表 service_group
DROP TABLE IF EXISTS `service_group`;
CREATE TABLE `service_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `name` varchar(32) NOT NULL,
  `comment` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- 表 case_set_service_groups
DROP TABLE IF EXISTS `case_set_service_groups`;
CREATE TABLE `case_set_service_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `caseset_id` int(11) NOT NULL,
  `servicegroup_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `caseset_id` (`caseset_id`,`servicegroup_id`),
  KEY `case_set_service_groups_7441409b` (`caseset_id`),
  KEY `case_set_service_groups_780d4012` (`servicegroup_id`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;

-- 表 judge_rule
DROP TABLE IF EXISTS `judge_rule`;
CREATE TABLE `judge_rule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `comment` varchar(255) NOT NULL,
  `simple_desc` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


-- 表 check_task
DROP TABLE IF EXISTS `check_task`;
CREATE TABLE `check_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `set_id` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT '0',
  `comment` varchar(255),
  `create_time` datetime,
  `execute_time` datetime,
  `product` varchar(32) NOT NULL,
  `is_pass` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- 表 check_result
DROP TABLE IF EXISTS `check_result`;
CREATE TABLE `check_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` int(11) NOT NULL,
  `execute_time` datetime NOT NULL,
  `case_id` int(11) NOT NULL,
  `url` longtext NOT NULL,
  `case_comment` varchar(255) NOT NULL,
  `comment` longtext NOT NULL,
  `is_pass` int(11) NOT NULL,
  `params` text,
  `rule` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `check_result_425ae3c4` (`task_id`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;

-- 表 product
DROP TABLE IF EXISTS `product`;
CREATE TABLE `product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;




