insert into judge_rule(id,name,comment,simple_desc) values(1,'UnanimousJudgeRule','所有机器响应结果必须一致,如果不一致则认为存在服务有错误','全一致规则');
insert into judge_rule(id,name,comment,simple_desc) values(2,'UnanimousWithFilterJudgeRule','***处理目标为XML***,会将某些XML的标签过滤掉，剩余部分必须完全一致','全一致规则(带过滤)');

insert into judge_rule(id,name,comment,simple_desc) values(3,'MeetExpectationForGJYQ','针对公交引擎,期望的导航路径出现在返回的结果集中','满足期望(公交引擎)');

insert into judge_rule(id,name,comment,simple_desc) values(4,'ExistSequence','必须存在一组指定的序列,序列的item可以由多个元素组成。使用此规则，有几个要素，首先需要指定包含序列的父级元素tag,然后需要指定包含item的元素tag,最后需要指明item中需要比较的元素的tag,如果存在多个，可以以逗号分隔。','存在序列规则');


-- insert into judge_rule(id,name,comment,simple_desc) values(5,'MeetExpectationForJCDH','针对驾车导航,期望的导航路径出现在返回的结果集中','满足期望(驾车导航)');

-- 增加权限-产品管理
insert into permission(codename,`desc`,type) values('product_manage','产品管理权限',1);






