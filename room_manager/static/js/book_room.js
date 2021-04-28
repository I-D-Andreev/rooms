$(document).ready(function(){
    let minDate = JSON.parse($("#min_date").text());
    $("#id_date").attr("min", minDate);

    let buildingSelect = $('#id_building');
    let floorsSelect = $('#id_floor');

    loadFloorsOnBuildingChange(buildingSelect, floorsSelect);
});