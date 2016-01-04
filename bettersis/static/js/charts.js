

function chart(){
    $('#loading_gif').show();
    var host = $( "#sel_host option:selected" ).val();
    var metric = $( "#sel_metric option:selected" ).val();
    var sitescope = $( "#sel_sitescope option:selected" ).val();


    var time_from = $('#date_from').data("DateTimePicker").date().format("D/M/YYYY HH:mm:ss");
    var time_to = $('#date_to').data("DateTimePicker").date().format("D/M/YYYY HH:mm:ss");

    queue()
    .defer(d3.json, "/json_chart/?host=" + host +
        "&metric=" + metric +
        "&time_from="+time_from +
        "&time_to=" + time_to +
        "&sitescope=" + sitescope)
    .await(makeGraphs);


}

$( document ).ready(function() {
    var loading_gif = $('#loading_gif');

    loading_gif.hide();
    $( "#btn_chart" ).click(function() {
        chart();
    });

    $('#sel_sitescope').on('change', function() {
        loading_gif.show();

        var sitescope = $( "#sel_sitescope option:selected" ).val();

        queue()
        .defer(d3.json, "/host_list/?sitescope=" + sitescope)
        .await(populateHostList);

    });

    $('#sel_ranges').on('change', function() {

        var dt_from = $('#date_from');
        var dt_to =  $('#date_to');
        var hora = new Date();
        var range = $( "#sel_ranges option:selected" ).val();

        dt_to.data("DateTimePicker").date(hora);

        if (range == "today"){
            hora.setHours(0,0,0,0);
            dt_from.data("DateTimePicker").date(hora);
        }
        else if(range == "yesterday"){
            hora.setHours(0,0,0,0);
            dt_to.data("DateTimePicker").date(hora);
            hora.setDate(hora.getDate() - 1);
            hora.setHours(0,0,0,0);
            dt_from.data("DateTimePicker").date(hora);
        }
        else if(range == "last7days"){
            hora.setDate(hora.getDate() - 6);
            hora.setHours(0,0,0,0);
            dt_from.data("DateTimePicker").date(hora);
        }
        else if(range == "bf2015"){
            dt_from.data("DateTimePicker").date(new Date(2015, 10, 26));
            dt_to.data("DateTimePicker").date(new Date(2015, 11, 1));
        }

        else if(range == "thisMonth") {
            dt_from.data("DateTimePicker").date(new Date(hora.getFullYear(), hora.getMonth(), 1));

        }



    });


    $(function () {
        var today = new Date();

        var dt_from = $('#date_from');
        var dt_to =  $('#date_to');

        dt_from.datetimepicker();
        dt_from.datetimepicker();
        dt_to.datetimepicker({
            useCurrent: false
        });

        dt_to.data("DateTimePicker").date(today);
        today.setHours(0,0,0,0);
        dt_from.data("DateTimePicker").date(today);

        dt_from.on("dp.change", function (e) {
            $('#date_to').data("DateTimePicker").minDate(e.date);
        });
        dt_to.on("dp.change", function (e) {
            $('#date_from').data("DateTimePicker").maxDate(e.date);
        });

         chart();
    });



});

function populateHostList(error, hosts){
    var loading_gif = $('#loading_gif');

    var $el = $("#sel_host");
    $el.empty(); // remove old options

    hosts.forEach(function(d) {
        $el.append($("<option></option>")
     .attr("value", d).text(d));
    });
    loading_gif.hide();

}

function makeGraphs(error, executions) {
    var metric = $( "#sel_metric option:selected" ).val();
    var chart_type = $( "#sel_type option:selected" ).val();
    var num_executions = executions.length;

    if (num_executions == 0){
            alert(num_executions + ' execuções encontradas');
           $('#loading_gif').hide();
        return;
    }

    executions.forEach(function(d) {

        var js_date =  new Date(d['fields']['time']);
	    js_date.setTime( js_date.getTime() + js_date.getTimezoneOffset()*60*1000 );
		d['fields']['time'] = js_date;

    });

    var ndx = crossfilter(executions);

    var dateDim = ndx.dimension(function(d) {
        return d['fields']['time'];
    });

    var minDate = dateDim.bottom(1)[0]['fields']['time'];
    var maxDate = dateDim.top(1)[0]['fields']['time'];

    var dateGroup = dateDim.group().reduceSum(function(d) {
        return d['fields']['value'];

    });


    if (chart_type == 'bar'){
        var timeChart = dc.barChart("#time-chart");
    }
    else if (chart_type == 'line'){
        var timeChart = dc.lineChart("#time-chart");
    }

	timeChart
		.width($(document).width() * 0.60)
		.height(320)
		.brushOn(false)
		.margins({top: 20, right: 150, bottom: 30, left: 100})
		.dimension(dateDim)
		.group(dateGroup)
		.x(d3.time.scale().domain([minDate,maxDate]))
		.elasticY(true)
		.yAxisLabel(metric)
		.xAxisLabel("Horario")
        .mouseZoomable(true)
		.xAxis().ticks(10);


    dc.renderAll();
    $('#loading_gif').hide();


}