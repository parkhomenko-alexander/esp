var chartButton = document.getElementById("chart-button");
var startDate = document.getElementById("date-start")
var startTime = document.getElementById("time-start");
var endDate = document.getElementById("date-end");
var endTime = document.getElementById("time-end");
var radioCo = document.getElementById("radio-co");
var radioTvoc = document.getElementById("radio-tvoc");


chartButton.addEventListener("click", function () {
    timeLineS = startDate.value + ' ' + startTime.value;
    timeLineE = endDate.value + ' ' + endTime.value;

    if (radioCo.checked) {
        var promise = axios.get('http://46.101.102.163:5000/data_manipulator/get_data_charts?chart_type=co&time_line_start=' + timeLineS +
            '&time_line_end=' + timeLineE);
    } else if (radioTvoc.checked) {
        var promise = axios.get('http://46.101.102.163:5000/data_manipulator/get_data_charts?chart_type=tvoc&time_line_start=' + timeLineS +
            '&time_line_end=' + timeLineE);
    } else {
        return;
    }

    promise.then((data) => {
        console.log(data.data);
        console.log(data.data['data_point']);
        console.log(data.data['average']);


        var dataPoints = data.data['data_point'];
        console.log(dataPoints)

        var chart = new CanvasJS.Chart("chartContainer", {
            theme: "light2",
            title: {
                text: data.data['type']
            },
            axisY: {
                titleFontColor: "#4F81BC",
                includeZero: true,
                suffix: "ppm",
                minimum: data.data['min_val'],
                maximum: data.data['max_val'] + 5
            },
            axisX: {
                minimum: 0
            },
            data: [{
                indexLabelFontColor: "darkSlateGray",
                name: "views",
                type: "splineArea",

                dataPoints: dataPoints
            }]
        });
        // .parametrs-with-chart
        var parameters = document.getElementById("parameters");
        parameters.classList.add('parameters-with-chart');
        document.getElementById("average").innerText = data.data['average'];
        if (data.data['average'] > data.data['normal']) {
            document.getElementById("average").style.backgroundColor = 'rgb(255, 65, 65)';
        }

        document.getElementById("max").innerText = data.data['max_val'];
        if (data.data['max_val'] > data.data['normal']) {
            document.getElementById("max").style.backgroundColor = 'rgb(255, 65, 65)';
        }

        document.getElementById("min").innerText = data.data['min_val'];
        console.log(data.data['min_val'], data.data['normal'])
        if (data.data['min_val'] > data.data['normal']) {
            document.getElementById("min").style.backgroundColor = 'rgb(255, 65, 65)';
        }


        chart.render();
    });
})



