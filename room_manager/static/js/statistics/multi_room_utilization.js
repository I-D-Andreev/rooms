$(document).ready(function(){
    $("#multi_room_utilization").css("font-weight", "bold");

    const UTILIZATION =  JSON.parse(document.getElementById("room_util").textContent);
    const DAYS = UTILIZATION["days"];

    let areasHolder = $("#areas_holder");
    
    for (let i=0; i < UTILIZATION.rooms.length; i++) {
        let chartId = `util_chart_${i}`;
        let roomId = UTILIZATION.rooms[i].id;
        let roomName = UTILIZATION.rooms[i].name;

        areasHolder.append(createChartElement(chartId));
        createPercentageChart(chartId, DAYS, `${roomName} Daily Percentage Utilization`, UTILIZATION[roomId]);
    }
});


function createChartElement(id){
    let el = `
        <div class="col-6">
            <canvas id="${id}" height="400" width="600" class="mt-5 mb-5"></canvas>
        </div>
    `;

    return el;
}
