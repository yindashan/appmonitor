function success(data){
	//$('#content').fadeOut();
	$("#content").html(data);
	//$('#content').fadeIn();
	docReady();
}
function error(data){
	alert('something is error!');	
}
//用来请求网页显示在固定位置
//　flag: 是否时左侧的主菜单
function executeMenu(element,flag){
	//alert(typeof(flag));
    if(flag){
	$('ul.main-menu li.active').removeClass('active');
	$(element).parent('li').addClass('active');	
	}

    var url = $(element).attr("href");
    jQuery.ajax({
        type: 'GET',
        url: url,
        success: success,
        error:error,
        dataType: 'html',
        async:false
    }); 
    return false;
}

//处理刷新页面，json字符串包含statusCode，url，message信息
function httpRedirect(data){
	var statusCode = data.statusCode;
	var url = data.url;
	var message = data.message;
	if (statusCode == 200){
		httpRedirectAjax(url);
	}
	alert(message);
}

//执行删除或批量删除
function executeDelete(obj,ids){
	var url = $(obj).attr("href");
	var message = $(obj).attr("title");
	if (!confirm(message))
  	{
  		return false;
  	}
    jQuery.ajax({
		type: 'POST',
		url: url,
		data:{'ids':ids},
		success:httpRedirect,
		error: error,
		dataType: 'json',
		async:false
	});	
	return false;
}
//请求url，刷新请求页面
function httpRedirectAjax(url){
    jQuery.ajax({
		type: 'GET',
		url: url,
		success: success,
		error:error,
		dataType: 'html',
		async:false
	});	
	return false;
}

//处理form表单,返回一个json字符串给httpRedirect函数进行重定向
function validateCallback(form){
	//校验失败，直接返回
	if(!$(form).valid()){
		alert("表单校验失败，无法提交!");
		return false;
	}
    var url = $(form).attr("action");
    jQuery.ajax({
		type: 'POST',
		url: url,
		data:$(form).serializeArray(),
		success: httpRedirect,
		error:error,
		dataType: 'json',
		async:false
	});	
	return false;
}

// 上一页，下一页
function pageJump(obj){
	//当前页,总页数	
	var url = $(obj).attr("href");
	var t = $(obj).parent().parent();
	var currPage = parseInt(t.attr("currPage"));
	var totalPage = parseInt(t.attr("totalPage"));
	var pageNum = 1;
	switch($(obj).parent().attr("class")){
		case "prev":
			if(currPage > 1){
				pageNum = currPage - 1;
			}else{
				pageNum = 1;
			}
			break;
		case "next":
			if(currPage < totalPage){
				pageNum = currPage + 1;
			}else{
				pageNum = totalPage;
			}
			break;
	}
	jQuery.ajax({
		type: 'POST',
		url: url,
		data:{'pageNum':pageNum},
		success:success,
		error: error,
		dataType: 'html',
		async:false
	});	
	return false;
}

// 用于权限配置页面
function validateCallback_role(form){
	//校验失败，直接返回
	if(!$(form).valid()){
		alert("表单校验失败，无法提交!");
		return false;
	}
    var url = $(form).attr("action");
    //serializeArray()返回结果是json对象
    data = $(form).serializeArray();
    // 获取组织机构树读权限
    nodes1 = $("#read_right_tree").tree('getCheckedExt'); //返回为json对象
    // 获取组织结构树操作权限
    nodes2 = $("#operate_right_tree").tree('getChecked');
    nodes = nodes1.concat(nodes2);
    for(var i=0;i<nodes.length;i++){
    	item = {"name":"permission_id","value":nodes[i].attributes.permission_id}
    	data.push(item);
    }
    jQuery.ajax({
		type: 'POST',
		url: url,
		data:data,
		success: httpRedirect,
		error:error,
		dataType: 'json',
		async:false,
	});	
	return false;
}
// 联合图配置管理
function validateCallback_combine(form){
	//校验失败，直接返回
	if(!$(form).valid()){
		alert("表单校验失败，无法提交!");
		return false;
	}
    var url = $(form).attr("action");
    //serializeArray()返回结果是json对象
    data = $(form).serializeArray();
    // 联合图所对应的数据源
    tr_array = $("#node_table2").find("tr");
    if(tr_array.length-1==0){
    	alert("必须配置关联的图表");
    	return false;
    }
    for(var i=1;i<tr_array.length;i++){
    	item = {"name":"chart_ids","value":$(tr_array[i]).attr("chart_id")}
    	data.push(item);
    }
    data.push()
    jQuery.ajax({
		type: 'POST',
		url: url,
		data:data,
		success: httpRedirect,
		error:error,
		dataType: 'json',
		async:false,
	});	
	return false;
}
//显示与所选应用对应的host和监控项
function node_config_success2(data){
	//重新设置下拉列表
	$("#host2 option:gt(0)").remove();
	$("#monitor2 option:gt(0)").remove();
	host_array = data.host_list
	monitor_array = data.monitor_list;
	//主机
	var i=0;
	for(i=0;i< host_array.length;i++){
		var t = $("<option></option>")
		t.val(host_array[i]);
		t.text(host_array[i]);
		$("#host2").append(t);
	}
	//监控项
	i=0;
	for(i=0;i< monitor_array.length;i++){
		var m = $("<option></option>")
		m.val(monitor_array[i].id);
		m.text(monitor_array[i].desc);
		$("#monitor2").append(m);
	}
}
//添加监控项
function do_combine_add(){
	//-------------------内部函数 定义----------------
	function getChartIdSuccess(data){
		chart_id = data;
	}
	//---------------------------------------------------

	var app_id = $("#app2").val();
	var monitor_id = $("#monitor2").val();
	var show_type = $("#show_type2").val();
	var app_text = $("#app2 option:selected").html();
	var host = $("#host2").val();
	var monitor_text = $("#monitor2 option:selected").html();
	var show_type_text = $("#show_type2 option:selected").text();
	//后面查询得到的值会覆盖此值
	var chart_id = "undefinded";
	//每一个选项都不能为空
	if(app_id&&host&&monitor_id&&show_type){
		var item = $("<tr></tr>");
		
		var app_td = $("<td></td>");
		app_td.text(app_text);
		item.append(app_td);
		
		var host_td = $("<td></td>");
		host_td.text(host);
		item.append(host_td);
		
		var monitor_td = $("<td></td>");
		monitor_td.text(monitor_text);
		item.append(monitor_td);
		
		var type_td = $("<td></td>");
		type_td.text(show_type_text)
		item.append(type_td);
		//删除
		item.append($("<td><button type='button' onclick='remove_item(this);' class='btn btn-mini btn-danger'>删除</button></td>"))
		
		//同步请求获取此showchart表记录的id
		data = {"app_id":app_id,"host":host,"monitor_id":monitor_id,"show_type":show_type};
		jQuery.ajax({
			type: 'GET',
			url: "/showchart/getChartId",
			data: data,
			success: getChartIdSuccess,
			error:error,
			dataType: 'text',
			async:false
		});
		item.attr("chart_id",chart_id);
		item.attr("monitor_id",monitor_id);
		//检查此item是否已存在
		tr_array = $("#node_table2").find("tr");
		for(var i=0;i<tr_array.length;i++){
			tr_id = $(tr_array[i]).attr("chart_id");
			if(tr_id==chart_id){
				//已存在
				alert("该图表已存在，无法添加");
				return;
			}
		}
		$("#node_table2").append(item);
	}else{
		alert("配置信息缺失!");
	}
}

//删除某个已选定的图表
function remove_item(obj){  
	$(obj).parent().parent().remove();
}

//----------------　搜索展示列表 -----------------
// ------------------- 用于搜索  ---------------------
//替换列表页面中的展示项
function search_success(data){
	//$('#content').fadeOut();
	
	var obj=$("#box-content div.row-fluid:first");
	$("#box-content").html(data);
	$("#box-content").prepend(obj);

	//$('#content').fadeIn();
	docReady();
}

//  搜索查询操作
function searchCallback(){

    //校验失败，直接返回
/*
    if(!$("form").valid()){
	alert("表单校验失败，无法提交!");
	return false;
    }
*/
    var url = $("#search_form").attr("action");
    jQuery.ajax({
	type: 'POST',
	url: url,
	data:$("form").serializeArray(),
	success: search_success,
	error:error,
	dataType:'html',
	async:false
     });
     return false;
}
//搜索结果页中的页面跳转,首页，末页，前一页，后一页，确定按钮
function searchPageJump(obj){
	//当前页,总页数	
	var url = $(obj).attr("href");
	var t = $(obj).parent().parent();
	var currPage = parseInt(t.attr("currPage"));
	var totalPage = parseInt(t.attr("totalPage"));
	var pageNum = 1;
	switch($(obj).parent().attr("class")){
		case "prev":
			if(currPage > 1){
				pageNum = currPage - 1;
			}else{
				pageNum = 1;
			}
			break;
		case "next":
			if(currPage < totalPage){
				pageNum = currPage + 1;
			}else{
				pageNum = totalPage;
			}
			break;
	}
	var param_data = $("form").serializeArray();
	param_data.push({'name':'pageNum','value':pageNum});
	jQuery.ajax({
		type: 'POST',
		url: url,
		data:param_data,
		success:search_success,
		error: error,
		dataType: 'html',
		async:false
	});	
	return false;
}

