$(document).ready(function(){
    enableDisableFields(true);

    $('#id_room').on('change', function(){
        let roomId = this.value;

        if (roomId === '') {
            fillFormData(null);
        }
        else {
            let url = `/get-room/${roomId}`
            $.ajax({
                url: url,
                success: function(data){
                    fillFormData(data);
                },
                error: function(err){
                    showErrorAlert(getAlertHolder(), "Could not load data!");
                    fillFormData(null);
                    console.log(err);
                }
            });
        }
    });

    $('#delete_room_prompt').on('click', function(){
        $('#delete_room_button').click();
    });

    fadePythonMessages();
});

function enableDisableFields(isDisabled) {
    $('#id_username').attr('disabled', isDisabled);
    $('#id_public_name').attr('disabled', isDisabled);
    $('#id_email').attr('disabled', isDisabled);
    $('#id_capacity').attr('disabled', isDisabled);
    $('#id_building').attr('disabled', isDisabled);
    $('#id_floor').attr('disabled', isDisabled);
}

function fillFormData(data) {
    clearFormData();

    if(data) {
        $('#id_username').val(data.username);
        $('#id_public_name').val(data.public_name);
        $('#id_email').val(data.email);
        $('#id_capacity').val(data.capacity);
        $('#id_building').val(data.buildingId);
        $('#id_floor').val(data.floorId);
    }
}


function clearFormData() {
    $('#id_username').val('');
    $('#id_public_name').val('');
    $('#id_email').val('');
    $('#id_capacity').val('');
    $('#id_building').val('');
    $('#id_floor').val('');
}


function getAlertHolder() {
    return $('#alert_holder');
}
