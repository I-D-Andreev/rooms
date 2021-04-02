var chart_daily = null;
var chart_weekly = null;
var chart_monthly = null;

$(document).ready(function(){
    const DAILY_UTILIZATION = JSON.parse(document.getElementById("daily_util").textContent);
    const DAYS = DAILY_UTILIZATION['days'];

    const WEEKLY_UTILIZATION = JSON.parse(document.getElementById("weekly_util").textContent);
    const WEEKS = WEEKLY_UTILIZATION['weeks'];


    let CHART_DAILY_ID = 'chart_daily';
    let CHART_WEEKLY_ID = 'chart_weekly';
    let CHART_MONTHLY_ID = 'chart_monthly';

    $('#id_room').on('change', function(){
        let roomId = this.value;
       
        if(roomId === "") {
            if (chart_daily !== null){
                chart_daily.destroy();
            }

            if (chart_weekly !== null){
                chart_weekly.destroy();
            }

            if (chart_monthly !== null){
                chart_monthly.destroy();
            }

        }
        else {
            // do stuff
            let roomName = $('#id_room :selected').text();
            let daily_data = DAILY_UTILIZATION[roomId];
            let weekly_data = WEEKLY_UTILIZATION[roomId]

            if(daily_data) {
                chart_daily = createPercentageChart(CHART_DAILY_ID, DAYS, `${roomName} Daily Percentage Utilization`, daily_data);
                // TODO: move
                chart_monthly = createPercentageChart(CHART_MONTHLY_ID, DAYS, `${roomName} Monthly Percentage Utilization`, daily_data);
            }

            if(weekly_data){
                chart_weekly = createPercentageChart(CHART_WEEKLY_ID, WEEKS, `${roomName} Weekly Percentage Utilization`, weekly_data);
            }
        }
    });

});

