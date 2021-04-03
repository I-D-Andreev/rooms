var chart_daily = null;
var chart_weekly = null;
var chart_monthly = null;

$(document).ready(function(){
    $("#room_utilization").css("font-weight", "bold");

    const DAILY_UTILIZATION = JSON.parse(document.getElementById("daily_util").textContent);
    const DAYS = DAILY_UTILIZATION['days'];

    const WEEKLY_UTILIZATION = JSON.parse(document.getElementById("weekly_util").textContent);
    const WEEKS = WEEKLY_UTILIZATION['weeks'];

    const MONTHLY_UTILIZATION = JSON.parse(document.getElementById("monthly_util").textContent);
    const MONTHS = MONTHLY_UTILIZATION['months'];

    const CHART_DAILY_ID = 'chart_daily';
    const CHART_WEEKLY_ID = 'chart_weekly';
    const CHART_MONTHLY_ID = 'chart_monthly';

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
            let roomName = $('#id_room :selected').text();
            let daily_data = DAILY_UTILIZATION[roomId];
            let weekly_data = WEEKLY_UTILIZATION[roomId];
            let monthly_data = MONTHLY_UTILIZATION[roomId];

            if (daily_data) {
                chart_daily = createPercentageChart(CHART_DAILY_ID, DAYS, `${roomName} Daily Percentage Utilization`, daily_data);
            }

            if (weekly_data) {
                chart_weekly = createPercentageChart(CHART_WEEKLY_ID, WEEKS, `${roomName} Weekly Percentage Utilization`, weekly_data);
            }

            if(monthly_data) {
                chart_monthly = createPercentageChart(CHART_MONTHLY_ID, MONTHS, `${roomName} Monthly Percentage Utilization`, monthly_data);
            }
        }
    });

});

