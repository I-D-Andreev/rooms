var lastFormData = null;

$(document).ready(function(){ 
    disableFillableFields(!$('#id_building').val());

    $('#id_building').on('change', function(){
        let buildingId = this.value;

        if (buildingId === '') {
            fillFormData(null);
            disableFillableFields(true);
        }
        else {
            let url = `/get-building/${buildingId}`
            $.ajax({
                url: url,
                success: function(data){
                    fillFormData(data);
                    disableFillableFields(false);
                },
                error: function(err){
                    showErrorAlert(getAlertHolder(), "Could not load data!");
                    fillFormData(null);
                    disableFillableFields(true);
                    console.log(err);
                }
            });
        }
    });
    

    $('#cancel_button').on('click', function(){
        fillFormData(lastFormData);
    });

    fadePythonMessages();
});



function fillFormData(data) {
    lastFormData = data;
    clearFormData();

    if (data) {
        $('#id_name').val(data.name);
        $('#id_description').val(data.description);
    }
}


function clearFormData() {
    $('#id_name').val('');
    $('#id_description').val('');
}


function getAlertHolder() {
    return $('#alert_holder');
}


function disableFillableFields(isDisabled){
    $('#id_name').attr('disabled', isDisabled);
    $('#id_description').attr('disabled', isDisabled);
}