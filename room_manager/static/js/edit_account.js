$(document).ready(function(){
    let buildingSelect = $('#id_building');
    let floorsSelect = $('#id_floor');

    loadFloorsOnBuildingChange(buildingSelect, floorsSelect);
})