delete from node_chart_relation;
delete from show_chart;
delete from show_node;
delete from app_service;
delete from monitor_item;
delete from auth_user;
delete from user_profile;
delete from role;
delete from role_users;
delete from role_permissions;
delete from ldapconf;
delete from permission;
delete from show_node_combineCharts;
delete from combine_chart;
delete from combine_chart_charts;


-- init
insert into show_node values(1,'高德软件',-1,1);
insert into ldapconf values(1,'ldap://10.2.145.102:389','dc=autonavi,dc=com','autonavi','sAMAccountName','service02','Service02');
-- 初始化用户
-- insert into auth_user (id,username,first_name,last_name,email,password,is_staff,is_active,is_superuser,last_login,date_joined) values (1,'admin','','','admin@autonavi.com','pbkdf2_sha256$10000$VG5dRIjUyzYs$3zQxkcVlHQXfpnqeDadQmBOwsbr3mvqN2zfTMfi6naE=',1,1,1,now(),now());

insert into auth_user (id,username,first_name,last_name,email,password,is_staff,is_active,is_superuser,last_login,date_joined) values (1,'admin','','','admin@autonavi.com','pbkdf2_sha256$10000$dVGcbP5yZs4x$yiXZoQiRbMHGfyA83RbEyZdNTs5EpRUuC1Pdsj7s9CA=',1,1,1,now(),now());

insert into user_profile (id,user_id,department,phone,realname) values (1,1,'高德软件','保密','admin');
insert into role_users values(1,1,1);
insert into role values(1,'系统管理员','系统管理员');
insert into permission values(1,'user_manage','用户管理权限',1);
insert into permission values(2,'role_manage','角色管理权限',1);
insert into permission values(3,'appitem_read','应用项读权限',2);
insert into permission values(4,'appitem_operate','应用项操作权限',2);
insert into permission values(5,'node_1_read','node',4);
insert into permission values(6,'node_1_operate','node',4);

insert into role_permissions values(1,1,1);
insert into role_permissions values(2,1,2);
insert into role_permissions values(3,1,3);
insert into role_permissions values(4,1,4);
insert into role_permissions values(5,1,5);
insert into role_permissions values(6,1,6);


-- 语义监控
insert into judge_rule(id,name,comment,simple_desc) values(1,'UnanimousJudgeRule','所有机器响应结果必须一致,如果不一致则认为存在服务有错误','全一致规则');
insert into judge_rule(id,name,comment,simple_desc) values(2,'UnanimousWithFilterJudgeRule','***处理目标为XML***,会将某些XML的标签过滤掉，剩余部分必须完全一致','全一致规则(带过滤)');

insert into judge_rule(id,name,comment,simple_desc) values(3,'MeetExpectationForGJYQ','针对公交引擎,期望的导航路径出现在返回的结果集中','满足期望(公交引擎)');

insert into judge_rule(id,name,comment,simple_desc) values(4,'ExistSequence','必须存在一组指定的序列,序列的item可以由多个元素组成。使用此规则，有几个要素，首先需要指定包含序列的父级元素tag,然后需要指定包含item的元素tag,最后需要指明item中需要比较的元素的tag,如果存在多个，可以以逗号分隔。','存在序列规则');


-- insert into judge_rule(id,name,comment,simple_desc) values(5,'MeetExpectationForJCDH','针对驾车导航,期望的导航路径出现在返回的结果集中','满足期望(驾车导航)');

-- 增加权限-产品管理
insert into permission values(150,'product_manage','产品管理权限',1);









