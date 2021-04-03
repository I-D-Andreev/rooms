

$(document).ready(function(){
    $("#busiest_hours").css("font-weight", "bold");
    
    const CHART_DAILY_ID = 'chart_daily';
    const CHART_WEEKLY_ID = 'chart_weekly';
    const CHART_MONTHLY_ID = 'chart_monthly';

    const BUSIEST_DAILY = JSON.parse(document.getElementById("busy_hours_daily").textContent);
    console.log(BUSIEST_DAILY)

    if (BUSIEST_DAILY) {
        createChart(CHART_DAILY_ID, BUSIEST_DAILY.hours, "Busiest Hours Today", BUSIEST_DAILY.hours_count);
    }


});
