//关闭图表搜索DIV
function close_watch_div(){
	$('#watch_div').modal('hide');
	$("#watch_div input").val("");
}
// 时间选择的快捷方式
function show_span_click(){
	var show_type = $(this).attr('show_type');
	//alert(show_type);
	var span_array = {'2':60*60*24,'3':60*60*24*30,'5':60*60*24*3,'6':60*60*24*7};
	var endTime = new Date().getTime(); // 单位毫秒
	var startTime = endTime - span_array[show_type]*1000;
	$("#startDateTime").val(new Date(startTime).format('yyyy-MM-dd hh:mm'));
	$("#endDateTime").val(new Date(endTime).format('yyyy-MM-dd hh:mm'));
}
// 按下watch_confirm 按钮
function watch_confirm_click(){
	var id = $("#hide_chartid").val();
	id = '#' + id;
	var chart_type = $(id).attr("chart_type");
	if((!$("#startDateTime").val())&&(!$("#endDateTime").val())){
		alert("开始时间和结束时间不能为空!");
		return;
	}
	$(id).attr('startDateTime',$("#startDateTime").val());
	$(id).attr('endDateTime',$("#endDateTime").val());

	$(id).attr('show_type',100);
	close_watch_div();
	//重新绘图
	print_chart("content");
}
