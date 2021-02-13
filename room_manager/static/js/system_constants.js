var SHOULD_SHOW_ID = "Specific Number Of Floors";

$(document).ready(function(){
    let typeSelect = $("#id_type");
    showOrHideFloors(typeSelect.val() == SHOULD_SHOW_ID)
    
    typeSelect.on('change', function(){
        let selectId = this.value;
        showOrHideFloors(selectId===SHOULD_SHOW_ID);
    });
    
});

function showOrHideFloors(shouldShow){
    
    let floorsInput = $("#floors_holder");

    if(shouldShow){
        floorsInput.show();
    } else {
        floorsInput.hide();
    }
}