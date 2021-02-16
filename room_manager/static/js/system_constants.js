var SHOULD_SHOW_FLOORS_ID = "Specific Number Of Floors";
var SHOULD_SHOW_INFER_ID = "This And Nearby Buildings";

var INITIAL_DATA = null;

$(document).ready(function(){
    let typeSelect = $("#id_type");
    
    typeSelect.on("change", function(){
        let selectId = this.value;
        showOrHideFloors(selectId===SHOULD_SHOW_FLOORS_ID);
        showOrHideInfer(selectId===SHOULD_SHOW_INFER_ID);
    });

    typeSelect.trigger('change');

    INITIAL_DATA = {
        "type": typeSelect.val(),
        "floors": $("#id_floors").val(),
        "infer": $("#id_infer_nearby_buildings").is(":checked")
    }

    $("#cancel_button").on("click", cancelButtonClicked);

    fadePythonMessages();
});

function cancelButtonClicked(){
    let typeSelect = $("#id_type");
    typeSelect.val(INITIAL_DATA.type);
    $("id_floors").val(INITIAL_DATA.floors);
    $("#id_infer_nearby_buildings").prop('checked', INITIAL_DATA.infer)

    typeSelect.trigger("change");
}


function showOrHideFloors(shouldShow){
    let floorsHolder = $("#floors_holder");
    let floors = $("#id_floors")

    if(floors.val() === ""){
        floors.val("0");
    }

    if(shouldShow){
        floorsHolder.show();
    } else {
        floorsHolder.hide();
    }
}

function showOrHideInfer(shouldShow){
    let inferHolder = $("#infer_holder");

    if(shouldShow){
        inferHolder.show();
    } else {
        inferHolder.hide();
    }
}