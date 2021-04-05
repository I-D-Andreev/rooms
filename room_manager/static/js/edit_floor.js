var lastFormData = null;

$(document).ready(function(){ 
    disableFillableFields(!$('#id_floor').val());
    setLastFormData();

    $('#id_floor').on('change', function(){
        let floorId = this.value;

        if (floorId === '') {
            fillFormData(null);
            disableFillableFields(true);
        }
        else {
            let url = `/get-floor/${floorId}`
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

function setLastFormData() {
    if ($("#id_floor").val() === '') {
        lastFormData = null;
    } else {
        lastFormData = {
            'name' : $("#id_name").val(),
        }
    }
}

function fillFormData(data) {
    lastFormData = data;
    clearFormData();

    if (data) {
        $('#id_name').val(data.name);
    }
}


function clearFormData() {
    $('#id_name').val('');
}


function getAlertHolder() {
    return $('#alert_holder');
}


function disableFillableFields(isDisabled){
    $('#id_name').attr('disabled', isDisabled);
}