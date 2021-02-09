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
            let url = `/get-room/${roomId}`
            $.ajax({
                url: url,
                success: function(data){
                    disableFillableFields(false);
                    fillFormData(data);
                },
                error: function(err){
                    console.log(err);
                }
            });

        }
    });

}

function fillFormData(data){
    if(data){
        $('#id_public_name').val(data.public_name);
        $('#id_email').val(data.email);
        $('#id_capacity').val(data.capacity);
        $('#id_building').val(data.buildingId);
        $('#id_floor').val(data.floorId);
    }
}

function disableFillableFields(isDisabled){
    $('#id_public_name').attr('disabled', isDisabled);
    $('#id_email').attr('disabled', isDisabled);
    $('#id_capacity').attr('disabled', isDisabled);
    $('#id_building').attr('disabled', isDisabled);
    $('#id_floor').attr('disabled', isDisabled);
}