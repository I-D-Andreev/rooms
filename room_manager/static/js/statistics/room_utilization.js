var chart_daily = null;
var chart_weekly = null;

$(document).ready(function(){
    const DAILY_UTILIZATION = JSON.parse(document.getElementById("daily_util").textContent);
    const DAYS = DAILY_UTILIZATION['days'];
    let CHART_DAILY_ID = 'chart_daily';
    let CHART_WEEKLY_ID = 'chart_weekly';

    $('#id_room').on('change', function(){
        let roomId = this.value;
       
        if(roomId === "") {
            if (chart_daily !== null){
                chart_daily.destroy();
            }

            if (chart_weekly !== null){
                chart_weekly.destroy();
            }

        }
        else {
            // do stuff
            let roomName = $('#id_room :selected').text();
            let data = DAILY_UTILIZATION[roomId];
            if(data) {
                chart_daily = createPercentageChart(CHART_DAILY_ID, DAYS, `${roomName} Daily Percentage Utilization`, data);
                chart_weekly = createPercentageChart(CHART_WEEKLY_ID, DAYS, `${roomName} Weekly Percentage Utilization`, data);
            }
        }
    });

});

