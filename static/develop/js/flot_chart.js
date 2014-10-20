//-----------全局变量----------- 
// 字典中的记录 按以下顺序排列 
// 4小时, 1天, 1个月，1年, 3天, 1周
//show_type_dict = {1:'4小时', 2:'1天', 3:'1个月', 4:'1年', 5:'3天', 6:'1周'}
//1) show_time  展示的时间长度 
//2) date_pattern 时间格式 
//3) cdp_interval  CDP 间隔

var chart_params = {'1':[60*60*4, '%H:%M', 60*5],'2':[60*60*24, '%H:%M', 60*5],'3':[60*60*24*31, '%m-%d', 60*30], '4':[60*60*24*365, '%m-%d', 60*60*6],'5':[60*60*24*3, '%m-%d %H:%M', 60*5],'6':[60*60*24*7, '%m-%d %H:%M', 60*5],'100':[60*60*24*31, '%m-%d %H:%M', 60*30]};

// 前一次鼠标hover的点
var previousPoint = null;
// 前一次鼠标hover的柱形
var previousLabel = null;

// 返回一个URL,通过此URL可以获得当前图表对应的时间区间内精确数据
function get_precise_data_url(obj){
	//-----------1.2 获取配置参数 --------------
	var show_type = $(obj).attr("show_type");
	//图表展示配置参数
	var deal_param = [];
	deal_param = chart_params[show_type];
  	var show_time = deal_param[0];   //展示的曲线的起至时间间隔
	
  	//以下数据用于取数据点
  	var ip = $(obj).attr("host_ip");
  	var app_name = $(obj).attr("app_name");
  	var monitor_item_id = $(obj).attr("monitor_item_id");
	
	//-----------1.3 计算显示的开始和结束时间--------------
	var showEndTime = null;
	var showStartTime = null;

	if(show_type==100){  //用户自定义时间区间 2012-12-13 00:00
		var start_str = $(obj).attr("startDateTime") + ":00";
		showStartTime = parseDate(start_str).getTime()/1000;

		var end_str = $(obj).attr("endDateTime")+":00";
		showEndTime = parseDate(end_str).getTime()/1000;

		var resolution_array = new Array(60*5, 60*30, 60*60*6);
		resolution = select_resolution(showEndTime - showStartTime,resolution_array);
	}else{
		//获取 当前时间 自1970 起经过的秒
		showEndTime = new Date().getTime()/1000;
		showEndTime = Math.floor(showEndTime)
		//计算  需要显示的开始时间
		showStartTime = showEndTime - show_time;
	}
	var template = "/rrd/precisedata/?ip={0}&app={1}&dsname={2}&start={3}&end={4}";
	var url = String.format(template, ip, app_name, 'monitor_id_' + monitor_item_id, showStartTime, showEndTime);
	//alert(url);
	return url;
}
//area 对那个区域(div)　内的图表进行更新
function print_chart(area){
  //alert(1);
  var target = ".flotchart"
  if(area){
  	target = '#' + area + ' ' + 'div' + target;
	//alert(target);
  }
  //------ import ---清除历史数据----
  var canvas_array = $(target);
  //alert('length = ' + canvas_array.length);
  // 0:单数据源曲线图 1:多数据源曲线图 2:多数据源饼图 3:多数据源柱形图
  for(var i=0;i<canvas_array.length;i++){
	var obj = canvas_array[i];
	var chart_type = $(obj).attr("chart_type");
	
	if(chart_type=="0"){
		drawSingleDSLineChart(obj);
	}else if(chart_type=="1"){
		drawMultiDSLineChart(obj);
	}else if(chart_type=="2"){
		drawMultiDSPieChart(obj);
	}else{
		drawMultiDSBarChart(obj);	
	}
  }
}


//单数据源曲线图
function drawSingleDSLineChart(obj){
	//################## 1. 准备数据  #################
	//-----------1.1 设置标题 --------------
	// Title
  	var chart_title = genChartTitle(obj);
	$(obj).parent().parent().find('h2').html('<i class="icon-list-alt"></i>' + ' ' + chart_title);
	
	//-----------1.2 获取配置参数 --------------
	var show_type = $(obj).attr("show_type");
	//图表展示配置参数
	var deal_param = [];
	deal_param = chart_params[show_type];
  	var show_time = deal_param[0];   //展示的曲线的起至时间间隔
  	var date_pattern = deal_param[1];
	
  	//以下数据用于取数据点
  	var ip = $(obj).attr("host_ip");
  	var app_name = $(obj).attr("app_name");
  	var monitor_item_id = $(obj).attr("monitor_item_id");
  	var resolution = deal_param[2];
	
	//-----------1.3 计算显示的开始和结束时间--------------
	var showEndTime = null;
	var showStartTime = null;

	if(show_type==100){  //用户自定义时间区间 2012-12-13 00:00
		var start_str = $(obj).attr("startDateTime") + ":00";
		showStartTime = parseDate(start_str).getTime()/1000;

		var end_str = $(obj).attr("endDateTime")+":00";
		showEndTime = parseDate(end_str).getTime()/1000;

		var resolution_array = new Array(60*5, 60*30, 60*60*6);
		resolution = select_resolution(showEndTime - showStartTime,resolution_array);
	}else{
		//获取 当前时间 自1970 起经过的秒
		showEndTime = new Date().getTime()/1000;
		showEndTime = Math.floor(showEndTime)
		//计算  需要显示的开始时间
		showStartTime = showEndTime - show_time;
	}
	
	//############### 2. 设置图中要显示的数据#################
	//---------label 标签-------
	var chart_labels = new Array();
	//---------图表上要显示的所有数据-------
    	var chart_data = new Array();
	//---------不同的曲线对应的颜色-------
	var chart_colors = new Array();
	
	
	// ########2.1  警告和错误 警戒线######
	config(obj,chart_labels,'warning',chart_data,chart_colors,"#f6f852","#f8fb03",showStartTime,showEndTime);
	config(obj,chart_labels,'critical',chart_data,chart_colors,"#fcbaba","#ff0000",showStartTime,showEndTime);

	//######## 2.2 设置监控项数据######
	//---------添加key对应的字符串--------------------
	chart_labels.push("monitior");
	//---------添加监控项对应曲线和key的颜色-------------
	chart_colors.push("#0000ff");
	
	var url ="/rrd/chartdata/"; 
	var data = {'ip':ip,
			'app':app_name,
			'dsname': 'monitor_id_' + monitor_item_id,
			'resolution':resolution,
			'start':showStartTime,
			'end':showEndTime
			};
    	jQuery.ajax({
		type: 'GET',
		url: url,
		data: data,
		success: data_success(chart_data),
		error:data_error,
		dataType: 'text',
		async:false
	});
	var label_data = [];
	for(var i=0;i<chart_labels.length;i++){
		var item={};
		item['label'] = chart_labels[i];
		// 由于 flotchart 只能显示UTC 时间,因此需要对时间作fake操作
		// +8hour
		for(var j=0;j<chart_data[i].length;j++){
			chart_data[i][j][0]=chart_data[i][j][0] + 60*60*8*1000;
		}
		item['data'] = chart_data[i];
		label_data.push(item);
	}
	//########3. 绘图 ######
	$.plot($(obj), label_data, {
		series: {
			lines: { show: true },
			points: { show: true,
				  radius: '1.0',
				  symbol: "circle"}
		},
		colors: chart_colors,
		xaxis: {
			mode: "time",
    			timeformat: date_pattern
		},
		grid: {
			hoverable: true,
			backgroundColor: { colors: ["#fff", "#eee"] }
		}
	});
	$(obj).bind("plothover",flot_hover);
}

//多数据源曲线图
function drawMultiDSLineChart(obj){
	//################## 1. 准备数据  #################
	//-----------1.1 设置标题 --------------
	// Title	
	var chart_title = genChartTitle(obj);
	$(obj).parent().parent().find('h2').html('<i class="icon-list-alt"></i>' + ' ' + chart_title);

	//-----------1.2 获取配置参数 --------------
	var show_type = $(obj).attr("show_type");
	//图表展示配置参数
	var deal_param = [];
	deal_param = chart_params[show_type];
  	var show_time = deal_param[0];   //展示的曲线的起至时间间隔
  	var date_pattern = deal_param[1];
  	var resolution = deal_param[2];
	
	//-----------1.3 计算显示的开始和结束时间--------------
	var showEndTime = null;
	var showStartTime = null;

	if(show_type==100){  //用户自定义时间区间 2012-12-13 00:00
		var start_str = $(obj).attr("startDateTime")+":00";
		showStartTime = parseDate(start_str).getTime()/1000;

		var end_str = $(obj).attr("endDateTime")+":00";
		showEndTime = parseDate(end_str).getTime()/1000;

		var resolution_array = new Array(60*5, 60*30, 60*60*6);
		resolution = select_resolution(showEndTime - showStartTime,resolution_array);
	}else{
		//获取 当前时间 自1970 起经过的秒
		showEndTime = new Date().getTime()/1000;
		showEndTime = Math.floor(showEndTime)
		//计算  需要显示的开始时间
		showStartTime = showEndTime - show_time;
	}
	
	//############### 2. 设置图中要显示的数据#################
	//---------label 标签-------
	var chart_labels = new Array();

	//---------图表上要显示的所有数据-------
    	var chart_data = new Array();

	//---------不同的曲线对应的颜色-------
	var chart_colors =  ['#EC0033','#A0D300','#FFCD00','#00B869','#999999','#FF7300','#004CB0'];
	//---------　数据源信息 --------
	//*********** ds_array 是json 对象 *********
	var ds_array = [];
	
	//2.1 提取数据源信息
	var chart_ids = $(obj).attr("chart_ids");
	var cid_array = chart_ids.split(',') 
	var url = "/showchart/getChartInfo/"
	for(var i=0;i<cid_array.length;i++){
		var data = {'chart_id':cid_array[i]};
	    	jQuery.ajax({
			type: 'GET',
			url: url,
			data: data,
			success: get_chartinfo_success(ds_array),
			error:data_error,
			dataType: 'json',
			async:false
		});
	}
	
	//2.2 获取监控数据
	url ="/rrd/chartdata/"; 
	//alert(ds_array.length);
	for(var i=0;i<ds_array.length;i++){
		
		var item = ds_array[i];
		var data = {		'ip':item.host_ip,
					'app':item.app_name,
					'dsname': 'monitor_id_' + item.monitor_item_id,
					'resolution':resolution,
					'start':showStartTime,
					'end':showEndTime
						};
	    	jQuery.ajax({
			type: 'GET',
			url: url,
			data: data,
			success: data_success(chart_data),
			error:data_error,
			dataType: 'text',
			async:false
		});
	}
	//2.3 曲线的标签
	var keys_desc = $(obj).attr("keys_desc");
	key_array = keys_desc.split(',');
	chart_labels = chart_labels.concat(key_array);

	var label_data = [];
	for(var i=0;i<chart_labels.length;i++){
		var item={};
		item['label'] = chart_labels[i];
		// 由于 flotchart 只能显示UTC 时间,因此需要对时间作fake操作
		// +8hour
		for(var j=0;j<chart_data[i].length;j++){
			chart_data[i][j][0]=chart_data[i][j][0] + 60*60*8*1000;
		}
		item['data'] = chart_data[i];
		label_data.push(item);
	}

	//########3. 绘图 ######
	$.plot($(obj), label_data, {
		series: {
			lines: { show: true },
			points: { show: true,
				  radius: '1.0',
				  symbol: "circle"}
		},
		colors: chart_colors,
		xaxis: {
			mode: "time",
    			timeformat: date_pattern
		},
		grid: {
			hoverable: true,
			backgroundColor: { colors: ["#fff", "#eee"] }
		}
	});
	$(obj).bind("plothover",flot_hover);
	
}
//多数据源饼图
function drawMultiDSPieChart(obj){
	//################## 1. 准备数据  #################
	//-----------1.1 设置标题 --------------
	// Title	
	var chart_title = genChartTitle(obj);
	$(obj).parent().parent().find('h2').html('<i class="icon-list-alt"></i>' + ' ' + chart_title);	

	//-----------1.2 获取配置参数 --------------
	var show_type = $(obj).attr("show_type");
	//图表展示配置参数
	var deal_param = [];
	deal_param = chart_params[show_type];
	//由于饼图和柱形图都是查看的某一时刻的的状态,所以resolution 和show_time 固定即可
	var resolution = 60*5;   //取数据点的时间间隔
	var show_time = 60*30;
	
	//-----------1.3 计算显示的开始和结束时间--------------
	var showEndTime = null;
	var showStartTime = null;

	if(show_type==100){  //用户自定义时间区间 2012-12-13 00:00
		var end_str = $("#targetDateTime").val()+":00";
		showEndTime = parseDate(end_str).getTime()/1000;

	}else{
		//获取 当前时间 自1970 起经过的秒
		showEndTime = new Date().getTime()/1000;
		showEndTime = Math.floor(showEndTime)
	}
	//计算  需要显示的开始时间
	showStartTime = showEndTime - show_time;
	
	//############### 2. 设置图中要显示的数据#################
	//---------label 标签-------
	var chart_labels = new Array();

	//---------图表上要显示的所有数据-------
    	var chart_data = new Array();

	//---------不同的曲线对应的颜色-------
	var chart_colors =  ['#EC0033','#A0D300','#FFCD00','#00B869','#999999','#FF7300','#004CB0'];
	//---------　数据源信息 --------
	//*********** ds_array 是json 对象 *********
	var ds_array = [];

	//2.1 提取数据源信息
	var chart_ids = $(obj).attr("chart_ids");
	var cid_array = chart_ids.split(',') 
	var url = "/showchart/getChartInfo/"
	for(var i=0;i<cid_array.length;i++){
		var data = {'chart_id':cid_array[i]};
	    	jQuery.ajax({
			type: 'GET',
			url: url,
			data: data,
			success: get_chartinfo_success(ds_array),
			error:data_error,
			dataType: 'json',
			async:false
		});
	}
	
	//2.2 获取监控数据
	url ="/rrd/chartdata/"; 
	//alert(ds_array.length);
	for(var i=0;i<ds_array.length;i++){
		
		var item = ds_array[i];
		var data = {		'ip':item.host_ip,
					'app':item.app_name,
					'dsname': 'monitor_id_' + item.monitor_item_id,
					'resolution':resolution,
					'start':showStartTime,
					'end':showEndTime
						};
	    	jQuery.ajax({
			type: 'GET',
			url: url,
			data: data,
			success: data_success2(chart_data),
			error:data_error,
			dataType: 'text',
			async:false
		});
	}
	
	//2.3 标签
	var keys_desc = $(obj).attr("keys_desc");
	key_array = keys_desc.split(',');
	chart_labels = chart_labels.concat(key_array);	


	var label_data = [];
	for(var i=0;i<chart_labels.length;i++){
		var item={};
		item['label'] = chart_labels[i];
		item['data'] = chart_data[i];
		label_data.push(item);
	}
	$.plot($(obj), label_data,
		{
			series: {
				pie: {
					show: true
				}
			},
			grid: {
				hoverable: true,
				autoHighlight:true
			},
			legend: {
				show: false
			}
		});
	
	$(obj).bind("plothover", pie_hover);

}

//多数据源柱形图
function drawMultiDSBarChart(obj){
	//################## 1. 准备数据  #################
	//-----------1.1 设置标题 --------------
	// Title	
	var chart_title = genChartTitle(obj);
	$(obj).parent().parent().find('h2').html('<i class="icon-list-alt"></i>' + ' ' + chart_title);	

	//-----------1.2 获取配置参数 --------------
	var show_type = $(obj).attr("show_type");
	//图表展示配置参数
	var deal_param = [];
	deal_param = chart_params[show_type];
	//由于饼图和柱形图都是查看的某一时刻的的状态,所以resolution 和show_time 固定即可
	var resolution = 60*5;   //取数据点的时间间隔
	var show_time = 60*30;
	
	//-----------1.3 计算显示的开始和结束时间--------------
	var showEndTime = null;
	var showStartTime = null;

	if(show_type==100){  //用户自定义时间区间 2012-12-13 00:00
		var end_str = $("#targetDateTime").val()+":00";
		showEndTime = parseDate(end_str).getTime()/1000;

	}else{
		//获取 当前时间 自1970 起经过的秒
		showEndTime = new Date().getTime()/1000;
		showEndTime = Math.floor(showEndTime)
	}
	//计算  需要显示的开始时间
	showStartTime = showEndTime - show_time;
	
	//############### 2. 设置图中要显示的数据#################
	//---------label 标签-------
	var chart_labels = new Array();

	//---------图表上要显示的所有数据-------
    	var chart_data = new Array();

	//---------不同的曲线对应的颜色-------
	var chart_colors =  ['#EC0033','#A0D300','#FFCD00','#00B869','#999999','#FF7300','#004CB0'];
	//---------　数据源信息 --------
	//*********** ds_array 是json 对象 *********
	var ds_array = [];

	//2.1 提取数据源信息
	var chart_ids = $(obj).attr("chart_ids");
	var cid_array = chart_ids.split(',') 
	var url = "/showchart/getChartInfo/"
	for(var i=0;i<cid_array.length;i++){
		var data = {'chart_id':cid_array[i]};
	    	jQuery.ajax({
			type: 'GET',
			url: url,
			data: data,
			success: get_chartinfo_success(ds_array),
			error:data_error,
			dataType: 'json',
			async:false
		});
	}
	
	//2.2 获取监控数据
	url ="/rrd/chartdata/"; 
	//alert(ds_array.length);
	for(var i=0;i<ds_array.length;i++){
		
		var item = ds_array[i];
		var data = {		'ip':item.host_ip,
					'app':item.app_name,
					'dsname': 'monitor_id_' + item.monitor_item_id,
					'resolution':resolution,
					'start':showStartTime,
					'end':showEndTime
						};
	    	jQuery.ajax({
			type: 'GET',
			url: url,
			data: data,
			success: data_success2(chart_data),
			error:data_error,
			dataType: 'text',
			async:false
		});
	}
	
	//2.3 曲线的标签
	var keys_desc = $(obj).attr("keys_desc");
	key_array = keys_desc.split(',');
	chart_labels = chart_labels.concat(key_array);	

	var dataset = [];
	var item = {};
	item['color'] = "#5482FF";
	var data = [];
	var ticks = [];
	for(var i=0;i<chart_data.length;i++){
		data.push([i,chart_data[i]]);
		ticks.push([i,chart_labels[i]]);
	}
	item['data'] = data;
	dataset.push(item);
	

	$.plot($(obj),dataset, {
		series: {
			bars: {
			show: true
			}
		},
		bars: {
			align: "left",
			barWidth: 0.5
		},
		xaxis: {          
  			ticks: ticks
		},
		grid: {
		        hoverable: true,
		        borderWidth: 2,
		        backgroundColor: { colors: ["#ffffff", "#EDF5FF"] }
		}

	});

      $(obj).bind("plothover", bar_hover);

}

//获取图表数据点失败执行此函数
function data_error(data){
    alert('获取图表数据点失败!');	
}

//　挑选合适resolution 取点的个数尽可能少，同时保证显示精度）
//[60*5,60*30,60*60*2,60*60*24]
function select_resolution(timespan,resoluton_array){
	var n = resoluton_array.length;
	var i =-1;
        var dp_num = 0;
	do{
	    i++;
	    dp_num = timespan/resoluton_array[i];
	}while(i<n-1&&dp_num>2000);
	return resoluton_array[i];
}

//data_type:   'warning' 'critical'
function config(obj,chart_labels,data_type,chart_data,chart_colors,min_color,max_color,start,end){
	var item_type = parseInt($(obj).attr(data_type + "_type"));
	
	switch (item_type){
	   case 1:
	   case 2:
   		//数据
   		var item = parseFloat($(obj).attr(data_type));
   		var item_data = [[start*1000,item],[end*1000,item]];
   		//----- 操作全局变量 --------
		//曲线标签
		chart_labels.push(data_type);
		//阀值曲线数据
		chart_data.push(item_data);
		//曲线的颜色
		chart_colors.push(max_color);
		break;
	   case 3:
	   case 4:
  		var item_min = parseFloat($(obj).attr(data_type + "_min"));
  		var item_max = parseFloat($(obj).attr(data_type + "_max"));
  		var item_min_data = [[start*1000,item_min],[end*1000,item_min]];
  		var item_max_data = [[start*1000,item_max],[end*1000,item_max]];
  		//----- 操作全局变量 --------
		//曲线标签
		chart_labels.push(data_type + "_min",data_type + "_max");
		////阀值曲线数据	
		chart_data.push(item_min_data,item_max_data);
		//曲线的颜色
		chart_colors.push(min_color,max_color);
		break;
	   default: 
   		alert("类型错误,只能是1,2,3,4 其中一种");
	}
}
//获取图表数据点成功执行此函数  曲线图
function data_success(data_array){
	//注意这里的用法
	function deal_data(data){
		data = data.replace(new RegExp("NaN", 'g'), "null");
		var obj =  jQuery.parseJSON(data);  
		var monitor_data = [];
		for (var i =0;i<obj.length ;i++ ){
		    	// 每一个离散点由四个值来表示    1. 时间 2.值 
			var temp = [obj[i].time*1000,obj[i].value];
			monitor_data.push(temp);
		}
		data_array.push(monitor_data);
	}
	return deal_data;
}
// 产生标题
function genChartTitle(obj){
	var array = ['4小时','1天','1个月','1年'];
	var app_name = $(obj).attr("app_name");
	var ip = $(obj).attr("host_ip");
	var desc = $(obj).attr("desc");
	var show_type = parseInt($(obj).attr("show_type"));
	var res = '';
	if(app_name&&ip){
		res += " " + app_name;	
		res += " " + ip;
	}
	res += " " + desc; 
	if(show_type <= array.length){
		res += ' ' + array[show_type-1];
	}
	return res;
}
//在曲线上浮动时，显示曲线坐标　
function flot_hover(event, pos, item) {
	if (item) {
		if (previousPoint != item.dataIndex) {
			previousPoint = item.dataIndex;
			$("#tooltip").remove();
			var x = item.datapoint[0];
			var y = item.datapoint[1].toFixed(2);

			showTooltip(item.pageX, item.pageY,
				'(' + new Date(x-60*60*8*1000).format('MM-dd hh:mm') +',' + y + ')');
		}
	}
	else {
		$("#tooltip").remove();
		previousPoint = null;
	}
}
function showTooltip(x, y, contents) {
	$('<div id="tooltip">' + contents + '</div>').css( {
		position: 'absolute',
		display: 'none',
		top: y + 5,
		left: x + 5,
		border: '1px solid #fdd',
		padding: '2px',
		'background-color': '#dfeffc',
		opacity: 0.80
	}).appendTo("body").fadeIn(200);
}

function showTooltip2(x, y, color, contents) {
    $('<div id="tooltip">' + contents + '</div>').css({
        position: 'absolute',
        display: 'none',
        top: y - 40,
        left: x - 120,
        border: '2px solid ' + color,
        padding: '3px',
        'font-size': '9px',
        'border-radius': '5px',
        'background-color': '#fff',
        'font-family': 'Verdana, Arial, Helvetica, Tahoma, sans-serif',
        opacity: 0.9
    }).appendTo("body").fadeIn(200);
}

// 记录数据源信息
function get_chartinfo_success(ds_array){
	function getinfo_inside(data){
		ds_array.push(data)
	}
	return getinfo_inside;
}
// 获取图表数据点成功执行此函数  饼图　柱形图
function data_success2(data_array){
	//注意这里的用法
	function deal_data(data){
		data = data.replace(new RegExp("NaN", 'g'), "null");
		var obj =  jQuery.parseJSON(data);  
		var i = obj.length-1;
		while(i>=0 && obj[i].value==null){
			i--;
		}
		if(i>=0){
			data_array.push(obj[i].value);
		}else{
			data_array.push(null);
		}
	}
    return deal_data;
}
// 饼图浮动提示 tooltip
function pie_hover(event, pos, item){
	if (item){
		if(previousLabel!=item.series.label){
			previousLabel = item.series.label;
			$("#tooltip").remove();
			var color = item.series.color;
			//var value = $.formatNumber(item.series.data[0][1], { format: "#,###", locale: "us" });
			showTooltip2(pos.pageX,pos.pageY,color, "此部分的值为" + item.series.data[0][1]);
		}

	}else{
		$("#tooltip").remove();
		previousPoint = null;
	}
}

// 柱形图浮动提示 tooltip
function bar_hover(event, pos, item) {
	if (item) {
	    if ((previousLabel != item.series.label) || (previousPoint != item.dataIndex)) {
		previousPoint = item.dataIndex;
		previousLabel = item.series.label;
		$("#tooltip").remove();

		var x = item.datapoint[0];
		var y = item.datapoint[1];

		var color = item.series.color;
		showTooltip2(item.pageX,item.pageY,color,item.series.xaxis.ticks[x].label + " : <strong>" + y + "</strong>");
	    }
	} else {
	    $("#tooltip").remove();
	    previousPoint = null;
	}
}

