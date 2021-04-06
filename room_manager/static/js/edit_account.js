$(document).ready(function(){
    let buildingSelect = $('#id_building');
    let floorsSelect = $('#id_floor');
    
    loadFloorsOnBuildingChange(buildingSelect, floorsSelect);
    
    $("#id_old_password").removeAttr("autofocus");
    floorsSelect.focus();
})