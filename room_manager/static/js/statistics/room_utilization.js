var chart = null;

$(document).ready(function(){
    const DAILY_UTILIZATION = JSON.parse(document.getElementById("daily_util").textContent);
    const DAYS = DAILY_UTILIZATION['days'];
    let CHART_ID = 'chart';

    $('#id_room').on('change', function(){
        let roomId = this.value;
       
        if(roomId === "") {
            if (chart !== null){
                chart.destroy();
            }
        }
        else {
            // do stuff
            let roomName = $('#id_room :selected').text();
            let data = DAILY_UTILIZATION[roomId];
            if(data) {
                chart = createPercentageChart(CHART_ID, DAYS, `${roomName} Percentage Utilization`, data);
            }
        }
    });

});

