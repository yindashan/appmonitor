-- 表　auth_group

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
);

-- 表　auth_group_permissions

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_425ae3c4` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`)
);

-- 表　auth_permission

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_1bb8f392` (`content_type_id`)
);

-- 表　auth_user

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
);

-- 表　auth_user_groups

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_403f60f` (`user_id`),
  KEY `auth_user_groups_425ae3c4` (`group_id`)
);

-- 表　auth_user_user_permissions

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_403f60f` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`)
);

-- 表　django_admin_log

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_403f60f` (`user_id`),
  KEY `django_admin_log_1bb8f392` (`content_type_id`)
);

-- 表　django_content_type

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
);

-- 表　django_session

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_3da3d3d8` (`expire_date`)
);

-- 表　django_site

DROP TABLE IF EXISTS `django_site`;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
);


-- 表　ldapconf

DROP TABLE IF EXISTS `ldapconf`;
CREATE TABLE `ldapconf` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server` varchar(64) NOT NULL,
  `base_dn` varchar(64) NOT NULL,
  `domainname` varchar(64) NOT NULL,
  `loginname` varchar(64) NOT NULL,
  `username` varchar(64) NOT NULL,
  `password` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
);

-- 表　log

DROP TABLE IF EXISTS `log`;
CREATE TABLE `log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime NOT NULL,
  `username` varchar(64) NOT NULL,
  `content` varchar(255) NOT NULL,
  `log_type` int(11) NOT NULL,
  `relate_id` int(11) DEFAULT NULL,
  `level` int(11) NOT NULL,
  PRIMARY KEY (`id`)
);

-- 表　app_service

DROP TABLE IF EXISTS `app_service`;
CREATE TABLE `app_service` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(64) NOT NULL,
  `desc` varchar(128) NOT NULL,
  `ip_list` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_name` (`app_name`)
);



-- 表　monitor_item

DROP TABLE IF EXISTS `monitor_item`;
CREATE TABLE `monitor_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `monitor_type` varchar(1),
  `var_name` varchar(32),
  `formula` varchar(128),
  `warning_threshold` varchar(32),
  `critical_threshold` varchar(32),
  `desc` varchar(128),
  `app_id` int(11),
  PRIMARY KEY (`id`),
  KEY `monitor_item_app_id` (`app_id`)
);





-- 表　node_chart_relation

DROP TABLE IF EXISTS `node_chart_relation`;
CREATE TABLE `node_chart_relation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `show_node_id` int(11) NOT NULL,
  `show_chart_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `node_chart_relation_show_node_id` (`show_node_id`),
  KEY `node_chart_relation_show_chart_id` (`show_chart_id`)
);

-- 表 permission

DROP TABLE IF EXISTS `permission`;
CREATE TABLE `permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codename` varchar(64) NOT NULL,
  `desc` varchar(255) NOT NULL,
  `type` int(11) NOT NULL,
  PRIMARY KEY (`id`)
);


-- 表 permission_users

DROP TABLE IF EXISTS `permission_users`;
CREATE TABLE `permission_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `permission_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `permission_id` (`permission_id`,`user_id`),
  KEY `permission_users_permission_id` (`permission_id`),
  KEY `permission_users_user_id` (`user_id`)
);




-- 表 role

DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `desc` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
);



-- 表　role_permissions

DROP TABLE IF EXISTS `role_permissions`;
CREATE TABLE `role_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `role_id` (`role_id`,`permission_id`),
  KEY `role_permissions_role_id` (`role_id`),
  KEY `role_permissions_permission_id` (`permission_id`)
);


-- 表 role_users

DROP TABLE IF EXISTS `role_users`;
CREATE TABLE `role_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `role_id` (`role_id`,`user_id`),
  KEY `role_users_role_id` (`role_id`),
  KEY `role_users_user_id` (`user_id`)
);



-- 表 show_chart

DROP TABLE IF EXISTS `show_chart`;
CREATE TABLE `show_chart` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `monitor_item_id` int(11) NOT NULL,
  `host_ip` varchar(20) NOT NULL,
  `show_type` int(11) NOT NULL,
  `app_id` int(11) NOT NULL,
  `app_name` varchar(64) NOT NULL,
  `status` int(11) NOT NULL,
   PRIMARY KEY (`id`)
);


-- 表 show_node

DROP TABLE IF EXISTS `show_node`;
CREATE TABLE `show_node` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(64) NOT NULL,
  `parent_id` int(11) NOT NULL,
  `level` int(11) NOT NULL,
  PRIMARY KEY (`id`)
);

-- 表 user_profile

DROP TABLE IF EXISTS `user_profile`;
CREATE TABLE `user_profile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `department` varchar(128),
  `phone` varchar(32),
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`)
);

-- 表 combine_chart

DROP TABLE IF EXISTS `combine_chart`;
CREATE TABLE `combine_chart` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `desc` varchar(255) NOT NULL,
  `type` int(11) NOT NULL,
  `app_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `combine_chart_app_id` (`app_id`)
);

-- 表 combine_chart_charts

DROP TABLE IF EXISTS `combine_chart_charts`;
CREATE TABLE `combine_chart_charts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `combinechart_id` int(11) NOT NULL,
  `chart_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `combinechart_id` (`combinechart_id`,`chart_id`),
  KEY `combine_chart_charts_combinechart_id` (`combinechart_id`),
  KEY `combine_chart_charts_chart_id` (`chart_id`)
);

-- 表 show_node_combineCharts

DROP TABLE IF EXISTS `show_node_combineCharts`;
CREATE TABLE `show_node_combineCharts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `shownode_id` int(11) NOT NULL,
  `combinechart_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `shownode_id` (`shownode_id`,`combinechart_id`),
  KEY `show_node_combineCharts_shownode_id` (`shownode_id`),
  KEY `show_node_combineCharts_combinechart_id` (`combinechart_id`)
);


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





-- #######################################modify##################################

-- 邮件和短信报警

alter table app_service add column email_list varchar(255) default '';

alter table app_service add column mobile_list varchar(255) default '';

alter table app_service add column alarmtype int default 0;

alter table app_service add column check_interval int default 5;

alter table app_service add column max_check_attempts int default 2;

-- user_profile 增加字段 realname  真实姓名

alter table user_profile add column realname varchar(32);





