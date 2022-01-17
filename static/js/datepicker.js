var chartButton = document.getElementById("chart-button");
var startDate = document.getElementById("date-start")
var startTime = document.getElementById("time-start");
var endDate = document.getElementById("date-start");
var endTime = document.getElementById("time-end");
var radioCo = document.getElementById("radio-co");
var radioTvoc = document.getElementById("radio-tvoc");


chartButton.addEventListener("click", function () {
    console.log(startDate.value + startTime.value);

    timeLineS = startDate.value + ' ' + startTime.value;
    timeLineE = endDate.value + ' ' + endTime.value;
    console.log(timeLineS, timeLineE);
    if (radioCo.checked) {
        var promise = axios.get('http://localhost:5000/get_data_charts?chart_type=co&time_line_start=' + timeLineS +
            '&time_line_end=' + timeLineE);
    } else if (radioTvoc.checked) {
        var promise = axios.get('http://localhost:5000/get_data_charts?chart_type=tvoc&time_linne=timeLine');
    } else {
        var promise = axios.get('http://localhost:5000/get_data_charts?chart_type=none');
    }

    promise.then((data) => {
        console.log(data)
    });
})

