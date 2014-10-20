function delete_item(obj){
	var t = $(obj).parent().parent();
	ids = $("#exist_item").attr("del_ids");
	if(ids){
		var arr = ids.split(',');
		arr.push(t.attr('id'));
		$("#exist_item").attr("del_ids",arr.join(','));
	}else{
		$("#exist_item").attr("del_ids",t.attr('id'));
	}
	//alert($("#exist_item").attr("del_ids"));
	t.remove();
}
// 添加测试用例
function add_case(){
	//针对编辑的情况，此处的实现是通过删除和新增来替代编辑
	$("tr.curr input[type=button].del_btn").click();


	//校验
	if($("#url").valid()==0){
		alert('输入参数不合法!');
		return;
	}
	var url = $("#url").val();
	var comment = $("#comment").val();
	var rule_id = parseInt($("#rule_id").val());
	
	//规则说明
	var rule_str = $("#rule_id :selected").text();
	//alert(rule_str);
	//额外参数 存成JSON 字符串
	item_list = $("#extra_params input:visible,#extra_params textarea:visible");
	dd = {}
	for(var i=0;i<item_list.length;i++){
		dd[$(item_list[i]).attr('name')] = $(item_list[i]).val();
	}
	//把数据存储在<tr>的data中
	//alert(JSON.stringify(dd));	
	
	var t = $("<tr></tr>");
	t.addClass('active_data');
	t.addClass('add_data');
	t.data('item_data',{'url':url,'comment':comment,'rule_id':rule_id,'params':JSON.stringify(dd)});
	if(url.length > 40){
		url = url.substr(0,38) +'...';
	}
	if(comment.length > 25){
		comment = comment.substr(0,22) +'...';
	}
	// url
	var temp = $("<td></td>")
	temp.html(url);
 	t.append(temp);
 	// comment
 	temp = $("<td></td>")
	temp.html(comment);
 	t.append(temp);
 	// rule
 	temp = $("<td></td>")
	temp.html(rule_str);
 	t.append(temp);
	// params
	temp = $("<td></td>")
	temp.html(JSON.stringify(dd));
	t.append(temp);
 	// 创建button
	temp = $("<td></td>")

        var btn=$("<input></input>");
	btn.val("编辑");
	btn.addClass("edit_btn");
	btn.attr("type","button");
	temp.append(btn);

	btn=$("<input></input>");
	btn.val("删除");
	btn.attr("type","button");
	btn.addClass("del_btn");
	temp.append(btn);

 	t.append(temp);

 	$("#exist_item").append(t);
	// 重新注册事件
	//删除
	$("tr.active_data input[type='button'].del_btn").click(function(){
	 	$(this).parent().parent().remove();
	});
	//编辑
	$("tr.active_data input[type='button'].edit_btn").click(function(){
		edit_case(this);	
	});
	
	//清除表单中的内容，取出blockUI
	$('#case_div_cancel').click();
}

function edit_case(obj){
	// 1.标记此服务项正在被编辑
	var t = $(obj).parent().parent();
	t.addClass("curr");

	// 2. 弹出浮动层
	$("#add_case").click();

	// 3.提取信息
	var item_data = null;
	if(t.attr("id")){
		//有id说明这些记录已经在数据库中存在
		item_data = JSON.parse(t.attr('json_data'));				
	
	}else{
		item_data = t.data('item_data');
	}
	// 1) url
	$('#url').val(item_data['url']);
	// 2) comment
	$('#comment').val(item_data['comment']);
	// 3) rule_id
	$('#rule_id').val(item_data['rule_id']);
	$("#rule_id").change();
	// 4) params
	param_dict = JSON.parse(item_data['params']);
	for(var key in param_dict){
		var template = "#extra_params input[name={0}],#extra_params textarea[name={1}]";
		var selector = String.format(template,key,key);
		//alert(selector);
		$(selector).val(param_dict[key]);
	} 
}
// 添加服务信息
function add_service_item(){
	//针对编辑的情况，此处的实现是通过删除和新增来替代编辑
	$("tr.curr input[type=button].del_btn").click();

	//校验
	if($("#ip,#port").valid()==0){
		alert('输入参数不合法!');
		return;
	}

	var yes_arr = {1:'是',0:'否'};
	// 机房
	var idc = parseInt($("#idc").val());
	// IP
	var ip = $("#ip").val();
	// port
	var port = parseInt($("#port").val());
	// 是否使用代理
	var is_use_proxy = $("#is_use_proxy").attr("checked");
	if(is_use_proxy=='checked'){
		is_use_proxy = 1;
	}else{
		is_use_proxy = 0;
	}
	var t = $("<tr></tr>");
	t.data('item_data',{'idc':idc,'ip':ip,'port':port,'is_use_proxy':is_use_proxy});
	t.addClass('active_data');
	t.addClass('add_data');
	// idc
	var temp = $("<td></td>");
	var idc_str = $("#idc :selected").text();
	temp.html(idc_str);
 	t.append(temp);
 	// ip
 	temp = $("<td></td>")
	temp.html(ip);
 	t.append(temp); 
 	// port
 	temp = $("<td></td>")
	temp.html(port);
 	t.append(temp);
 	// is_use_proxy
 	temp = $("<td></td>")
	temp.html(yes_arr[is_use_proxy]);
 	t.append(temp);
	// 创建button
	temp = $("<td></td>")

        var btn=$("<input></input>");
	btn.val("编辑");
	btn.addClass("edit_btn");
	btn.attr("type","button");
	temp.append(btn);

	btn=$("<input></input>");
	btn.val("删除");
	btn.attr("type","button");
	btn.addClass("del_btn");
	temp.append(btn);
 	
	t.append(temp);
 	$("#exist_item").append(t);
	
	// 重新注册事件
	//删除
	$("tr.active_data input[type='button'].del_btn").click(function(){
	 	$(this).parent().parent().remove();
	});
	//编辑
	$("tr.active_data input[type='button'].edit_btn").click(function(){
		edit_service_item(this);	
	});
	
	//清除表单中的内容，取出blockUI
	$('#service_div_cancel').click();
}

// 触发编辑按钮时，执行此函数
function edit_service_item(obj){
	// 1.标记此服务项正在被编辑
	var t = $(obj).parent().parent();
	t.addClass("curr");
	// 2. 弹出浮动层
	$("#add_service").click();
	// 3.提取信息
	var item_data = null;
	if(t.attr("id")){
		//有id说明这些记录已经在数据库中存在
		item_data = JSON.parse(t.attr('json_data'));				
	
	}else{
		item_data = t.data('item_data');
	}
	// 1) idc
	$('#idc').val(item_data['idc']);
	// 2) ip
	$('#ip').val(item_data['ip']);
	// 3) port
	$('#port').val(item_data['port']);
	// 4) is_use_proxy
	if(item_data['is_use_proxy']==0){
		$('#is_use_proxy').attr("checked", false);
	}	
}
//处理form表单,返回一个json字符串给httpRedirect函数进行重定向
function validateCallback2(form){
	//校验失败，直接返回
	if(!$(form).valid()){
		alert("表单校验失败，无法提交!");
		return false;
	}
    var url = $(form).attr("action");
    var data = $(form).serializeArray();
    var tr_array = $("tr.add_data");
    var obj_list = [];
    var i =0;
    for(i =0;i<tr_array.length;i++){
		var item = $(tr_array[i]).data("item_data");
		obj_list.push(item);
    }
    //change to JSON String
    obj_list = JSON.stringify(obj_list)
    data.push({'name':'obj_list','value':obj_list});
    data.push({'name':'ids','value':$("#exist_item").attr("del_ids")});
    jQuery.ajax({
		type: 'POST',
		url: url,
		data:data,
		success: httpRedirect,
		error:error,
		dataType: 'json',
		async:false
	});	
	return false;
}

// 添加tab
function add_tab(obj){
	var url = $(obj).attr("href");
	//传递参数
	$("#mytabs").attr('cid',$(obj).attr("cid"));
	jQuery.ajax({
		type: 'GET',
		url: url,
		success: do_add_tab,
		error:error,
		dataType: 'html',
		async:false
	});	
	return false;
}
function do_add_tab(data){
	var tabs = $("#mytabs");
	var tabTitle = '测试用例' + $("#mytabs").attr('cid');
	var anchor = "fragment-" + $("#mytabs").attr('cid');
	//检查一下，指定的tab 是否已经打开
	if($('#'+anchor).length > 0){
		alert('相关tab已打开');
		return;	
	}
	var tabContent = data;
	var tabTemplate = "<li><a href='#{href}'>#{label}</a> <span class='ui-icon ui-icon-close' role='presentation'>Remove Tab</span></li>";
	var li = $( tabTemplate.replace( /#\{href\}/g, '#' + anchor).replace( /#\{label\}/g, tabTitle ) );
	tabs.find( ".ui-tabs-nav" ).append(li);
	// newtab
	var newtab = $("<div></div>");
	newtab.html(decodeHTML(data));
	//alert(newtab.html());
	newtab.attr('id',anchor);
	tabs.append(newtab);
	tabs.tabs( "refresh" );

	// 重新注册关闭按钮的动作
	$("span.ui-icon-close").click(function(){
		var panelId = $(this).closest("li").remove().attr('aria-controls');
	      	$( "#" + panelId ).remove();
	      	$("#mytabs").tabs("refresh");
	});
}
