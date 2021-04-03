var chart_daily = null;
var chart_weekly = null;
var chart_monthly = null;

$(document).ready(function(){
    $("#room_busiest_hours").css("font-weight", "bold");

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
            let daily_data = null;
            let weekly_data = null;
            let monthly_data = null;

            if (daily_data) {
                // chart_daily = createPercentageChart(CHART_DAILY_ID, DAYS, `${roomName} Daily Percentage Utilization`, daily_data);
            }

            if (weekly_data) {
                // chart_weekly = createPercentageChart(CHART_WEEKLY_ID, WEEKS, `${roomName} Weekly Percentage Utilization`, weekly_data);
            }

            if(monthly_data) {
                // chart_monthly = createPercentageChart(CHART_MONTHLY_ID, MONTHS, `${roomName} Monthly Percentage Utilization`, monthly_data);
            }
        }
    });

});
