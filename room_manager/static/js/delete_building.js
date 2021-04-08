$(document).ready(function(){ 
    disableFields();

    $('#id_building').on('change', function(){
        let buildingId = this.value;

        if (buildingId === '') {
            fillFormData(null);
        }
        else {
            let url = `/get-building/${buildingId}`
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

    $('#cancel_button').on('click', function(){
        $("#id_building").val('');
        $("#id_building").trigger('change');
    });


    fadePythonMessages();
});

function fillFormData(data) {
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

function disableFields() {
    $('#id_name').attr('disabled', true);
    $('#id_description').attr('disabled', true);
}

function getAlertHolder() {
    return $('#alert_holder');
}
