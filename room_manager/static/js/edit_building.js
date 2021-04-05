var lastFormData = null;

$(document).ready(function(){ 
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