$(document).ready(function(){
    enableDisableFields(true);

    $('#id_profile').on('change', function(){
        let profileId = this.value;

        if (profileId === '') {
            fillFormData(null);
        }
        else {
            let url = `/get-user-info/${profileId}`
            $.ajax({
                url: url,
                success: function(data){
                    fillFormData(data);
                    console.log(data);
                },
                error: function(err){
                    showErrorAlert(getAlertHolder(), "Could not load data!");
                    fillFormData(null);
                    console.log(err);
                }
            });
        }
    });
});

function enableDisableFields(isDisabled) {
    $('#id_username').attr('disabled', isDisabled);
    $('#id_public_name').attr('disabled', isDisabled);
    $('#id_email').attr('disabled', isDisabled);
    $('#id_building').attr('disabled', isDisabled);
    $('#id_floor').attr('disabled', isDisabled);
}

function fillFormData(data) {
    clearFormData();

    if (data) {
        $('#id_username').val(data.username);
        $('#id_public_name').val(data.public_name);
        $('#id_email').val(data.email);
        $('#id_building').val(data.building_id);
        $('#id_floor').val(data.floor_id);
    }
}

function clearFormData() {
    $('#id_username').val('');
    $('#id_public_name').val('');
    $('#id_email').val('');
    $('#id_building').val('');
    $('#id_floor').val('');
}


function getAlertHolder() {
    return $('#alert_holder');
}
