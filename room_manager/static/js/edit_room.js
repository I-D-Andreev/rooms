var lastFormData = null;

$(document).ready(function(){
    let buildingSelect = $('#id_building');
    let floorsSelect = $('#id_floor');
    
    disableFillableFields(!$('#id_room').val());
    setLastFormData();

    attachCancelButton($("#cancel_button"));
    loadFloorsOnBuildingChange(buildingSelect, floorsSelect);
    loadRoomOnSelectChange();
    fadePythonMessages();
})


function attachCancelButton(button){
    button.on('click', function(){
        fillFormData(lastFormData);
    });
}

function loadRoomOnSelectChange(){
    $('#id_room').on('change', function(){
        let roomId = this.value;
        if(roomId === ''){
            disableFillableFields(true);
            fillFormData(null);
        } else {
            let url = `/get-room/${roomId}`
            $.ajax({
                url: url,
                success: function(data){
                    disableFillableFields(false);
                    fillFormData(data);
                },
                error: function(err){
                    showErrorAlert(getAlertHolder(), "Could not load data!");
                    disableFillableFields(true);
                    fillFormData(null);
                    console.log(err);
                }
            });

        }
    });

}

function setLastFormData() {
    if($('#id_room').val() === '') {
        lastFormData = null;
    } else {
        lastFormData = {
            'public_name': $('#id_public_name').val(),
            'email': $('#id_email').val(),
            'capacity': $('#id_capacity').val(),
            'buildingId': $('#id_building').val(),
            'floorId': $('#id_floor').val(),
        };
    }
}


function fillFormData(data){
    lastFormData = data;
    clearFormData();

    if(data){
        $('#id_public_name').val(data.public_name);
        $('#id_email').val(data.email);
        $('#id_capacity').val(data.capacity);
        $('#id_building').val(data.buildingId);
        $('#id_floor').val(data.floorId);
    }
}

function clearFormData(){
    $('#id_public_name').val('');
    $('#id_email').val('');
    $('#id_capacity').val('');
    $('#id_building').val('');
    $('#id_floor').val('');

}

function disableFillableFields(isDisabled){
    $('#id_public_name').attr('disabled', isDisabled);
    $('#id_email').attr('disabled', isDisabled);
    $('#id_capacity').attr('disabled', isDisabled);
    $('#id_building').attr('disabled', isDisabled);
    $('#id_floor').attr('disabled', isDisabled);
}

function getAlertHolder() {
    return $('#alert_holder');
}