var chart = echarts.init(document.getElementById('ncov-map'), 'white', {renderer: 'canvas'});
// var p_chart = echarts.init(document.getElementById('pmap-chart'), 'white', {renderer: 'canvas'});
var loader = document.getElementById('loading');
var time_index = 0;
var start_index = 0;
var iframe = document.getElementById('pmap-chart');
iframe.onreadystatechange=function() {
		//此事件在内容没有被载入时候也会被触发，所以我们要判断状态
		//有时候会比较怪异 readyState状态会跳过 complete 所以我们loaded状态也要判断
        loader.css.dispaly = "";
		if (iframe.readyState === "complete" || iframe.readyState === "loaded"){
		    loader.css.dispaly = "none"
        }
	};


$(
    function () {
        chart.showLoading();
        // updateOverall();
        //
        fetchData(chart);
        updateNews();

        // setInterval(updateNews, 60 * 1000);
        // setInterval(updateOverall, 60 * 1000);
        // setInterval(fetchData, 30 * 60 * 1000);
    }
);
chart.on('click', function(params){
    if (isNaN(params.name.charAt(0))){
        $.ajax({
            type: "GET",
            url: getHost() + "/pmap",
            data: {"prov_name": params.name, "time_index":time_index, "start_index": start_index},
            dataType: "html",
            success: function (result) {
                var blob = new Blob([result], {'type': 'text/html'});
                iframe.src = URL.createObjectURL(blob);
                var myModal = $("#chart-modal");
                myModal.modal("show");
            }
        });

    }
});


chart.on('timelinechanged', function(params) {
    time_index = params.currentIndex;
    fetchData();
    updateNews();

});

function getHost() {
    return document.location.protocol + "//" +window.location.host;
}

function updateOverall(){
    $.ajax({
        type: "GET",
        url: getHost() + "/overall",
        dataType: 'json',
        success: function (result) {
            var t = new Date()

            overall_html = '<li class="text-muted"><i class="fa fa-bug pr-2"></i>' + result['results'][0]['note1'] + '</li><li class="text-muted"><i class="fa fa-hospital-o pr-2"></i>  疑似病例：' + result['results'][0]['suspectedCount'] + '</li><li class="text-muted"><i class="fa fa-heartbeat pr-2"></i>确诊病例：' + result['results'][0]['confirmedCount'] + '</li><li class="text-muted"><i class="fa fa-hospital-o pr-2"></i>死亡病例：' + result['results'][0]['deadCount'] + '</li><li class="text-muted"><i class="fa fa-clock-o pr-2"></i>更新时间：' + result['time'] + '</li>'
            $('#overall').html(overall_html)
        }
    });
}

function updateNews(){
    $.ajax({
        type: "GET",
        url: getHost() + "/news",
        data: {"time_index":time_index, "start_index": start_index},
        dataType: 'json',
        success: function (result) {
            // window.alert(result['news']);
            news_html = result['date'];
            for(var i = 0, len = result['news'].length; i < len; i++){


                news_html += "<li><div class='flex-Introduction'>" + result['news'][i] + "</a></div><small class='text-muted'></small></li>"

                // news_html += "<li><div class='base-timeline-info'>" + result[i] + "</a></div><small class='text-muted'></small></li>"
            }
            $('#newslist').html(news_html)
        }
    });
}

function fetchData() {
    $.ajax({
        type: "GET",
        url: getHost() + "/map",
        data: {"time_index":time_index, "start_index": start_index},
        dataType: 'json',
        success: function (result) {
            chart.hideLoading();
            start_index = result['st_ind'];
            time_index = result['ind'];
            chart.setOption(result['lock_map']);
        }
    });
}
