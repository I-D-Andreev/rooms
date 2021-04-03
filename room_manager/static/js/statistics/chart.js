function createChart(chartId, labels, chartLabel,  data) {
    return __createChart(chartId, labels, chartLabel, data);
}

function createBusiestHoursChart(chartId, labels, chartLabel,  data) {
    let scales = {
        yAxes: [{
            ticks: {
                suggestedMin: 0,
                suggestedMax: 20,
            },
            scaleLabel: {
                display: true,
                labelString: "Number of Bookings"
            },
        }]
    };


    return __createChart(chartId, labels, chartLabel,  data, scales)
}


function createPercentageChart(chartId, labels, chartLabel,  data) {
    let scales = {
        yAxes: [{
            ticks: {
                min: 0,
                max: 100,
                callback: (val) => {return val + "%";}
            },
        
            scaleLabel: {
                display: true,
                labelString: "Percentage"
            },
        }]
    };

    return __createChart(chartId, labels, chartLabel, data, scales=scales);
}


function __createChart(chartId, labels, chartLabel,  data, scales = null) {
    if (!scales) {
        scales = {
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                }
            }]
        };
    }

    var canvas = document.getElementById(chartId);

    var chart = new Chart(canvas, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: chartLabel,
                data: data,
                backgroundColor: 'rgba(0, 255, 0, 0.2)',
                borderWidth: 2,
                pointHitRadius: 10,

            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            scales: scales,
        }
    });

    return chart;
}
