var chartButton = document.getElementById("chart-button");

var startDate = document.getElementById("date-start")
var startTime = document.getElementById("time-start");
var endDate = document.getElementById("date-end");
var endTime = document.getElementById("time-end");

var dataList = 0;

chartButton.addEventListener("click", function () {
    timeLineS = startDate.value + ' ' + startTime.value;
    timeLineE = endDate.value + ' ' + endTime.value;

    var promise = axios.get('http://localhost:5000/get_data?time_line_start=' + timeLineS + '&time_line_end=' + timeLineE);

    promise.then((data) => {
        console.log(data.data);
        console.log(data.data['data_point']);

        var dataPoints = data.data['data_point'];
        console.log(dataPoints)

    });
})
