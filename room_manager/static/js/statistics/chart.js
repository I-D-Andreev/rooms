function createChart(chartId, labels, chartLabel,  data) {
    return __createChart(chartId, labels, chartLabel, data);
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


    var ctx = document.getElementById(chartId);

    var chart = new Chart(ctx, {
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
            responsive:true,
            maintainAspectRatio: false,
            scales: scales,
        }
    });

    return chart;
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
