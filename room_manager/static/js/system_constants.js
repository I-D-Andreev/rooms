var SHOULD_SHOW_ID = "Specific Number Of Floors";
var INITIAL_DATA = null;

$(document).ready(function(){
    let typeSelect = $("#id_type");
    showOrHideFloors(typeSelect.val() == SHOULD_SHOW_ID)
    
    typeSelect.on("change", function(){
        let selectId = this.value;
        showOrHideFloors(selectId===SHOULD_SHOW_ID);
    });

    INITIAL_DATA = {
        "type": typeSelect.val(),
        "floors": $("#id_floors").val()
    }

    $("#cancel_button").on("click", cancelButtonClicked);
});

function cancelButtonClicked(){
    let typeSelect = $("#id_type");
    typeSelect.val(INITIAL_DATA.type);
    $("id_floors").val(INITIAL_DATA.floors);

    typeSelect.trigger("change");
}


function showOrHideFloors(shouldShow){
    
    let floorsInput = $("#floors_holder");

    if(shouldShow){
        floorsInput.show();
    } else {
        floorsInput.hide();
    }
}