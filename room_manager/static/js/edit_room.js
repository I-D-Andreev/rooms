$(document).ready(function(){
    let buildingSelect = $('#id_building');
    let floorsSelect = $('#id_floor');


    loadFloorsOnBuildingChange(buildingSelect, floorsSelect);
    loadRoomOnSelectChange();
    disableFillableFields(true);
})

function loadRoomOnSelectChange(){
    $('#id_room').on('change', function(){
        let roomId = this.value;
        if(roomId === ''){
            disableFillableFields(true);
        } else {
            disableFillableFields(false);

            
        }
    });

}


function disableFillableFields(isDisabled){
    $('#id_public_name').attr('disabled', isDisabled);
    $('#id_email').attr('disabled', isDisabled);
    $('#id_capacity').attr('disabled', isDisabled);
    $('#id_building').attr('disabled', isDisabled);
    $('#id_floor').attr('disabled', isDisabled);
}