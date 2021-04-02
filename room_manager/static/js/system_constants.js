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
        "infer": $("#id_infer_nearby_buildings").is(":checked"),
        "start_hour": $("#id_start_work_hour").val(),
        "start_minute": $("#id_start_work_minute").val(),
        "end_hour": $("#id_end_work_hour").val(),
        "end_minute": $("#id_end_work_minute").val(),
    }

    $("#cancel_button_room_distance").on("click", cancelButtonRoomDistanceClicked);
    $("#cancel_button_work_hours").on("click", cancelButtonWorkHoursClicked);

    $('[data-toggle="tooltip"]').tooltip()
    
    fadePythonMessages();
});

function cancelButtonRoomDistanceClicked(){
    let typeSelect = $("#id_type");
    typeSelect.val(INITIAL_DATA.type);
    $("id_floors").val(INITIAL_DATA.floors);
    $("#id_infer_nearby_buildings").prop('checked', INITIAL_DATA.infer)

    typeSelect.trigger("change");
}

function cancelButtonWorkHoursClicked() {
    $("#id_start_work_hour").val(INITIAL_DATA.start_hour);
    $("#id_start_work_minute").val(INITIAL_DATA.start_minute);

    $("#id_end_work_hour").val(INITIAL_DATA.end_hour);
    $("#id_end_work_minute").val(INITIAL_DATA.end_minute);
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