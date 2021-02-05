var buildingId = "";

$(document).ready(function(){
    enableButtons(false);

    $('#id_building').on('change', function(){
        buildingId = this.value;
        showFloors();        
    });

    $('#add_floor').on('click', addFloor);
    $('#save_floors').on('click', saveFloors);

    // Focus text area when prompt shows.
    $('#add_floor_prompt').on('shown.bs.modal', function(){
        let floorNameArea =$('#floor_name_textarea'); 
        floorNameArea.val('');
        floorNameArea.focus();
    });

    // 'Click' Add Floor button on enter click when prompt is shown.
    $('#floor_name_textarea').on('keydown', function(event){

        if(event.keyCode === 13){
            $('#add_floor').click();
            event.preventDefault();
        }
    })
});

function enableButtons(isEnabled){
    $('#save_floors').attr("disabled", !isEnabled);
    $('#add_floor_prompt_button').attr("disabled", !isEnabled);
}

function showFloors(){
    if(buildingId === ""){
        renderFloorData(null);
        enableButtons(false);
    } else {
        enableButtons(true);

        $.ajax({
            url: `/get-building-floors/${buildingId}`,
            success: function(data){
                console.log(data);
                renderFloorData(data);
            },
            error: function(err){
                console.log(err);
            }
        });
    }
}


function renderFloorData(floorsList){
    floorsContainer = $('#floors');

    // remove child elements
    floorsContainer.empty();

    if(floorsList !== null){
        if(floorsList.length > 0){
            for(let i=floorsList.length-1; i>=0; i--){
                floorsContainer.append(createFloorElement(floorsList[i].name));
            }
        }
        else {
            let element = `
            <div id="no_floors">
                <h4> No floors </h4>
            </div>
        `;
            floorsContainer.append(element);
        }
    }
}


function addFloor(){
    let floorNameArea =$('#floor_name_textarea'); 
    let floorsContainer = $('#floors');

    let floorName = floorNameArea.val();
    
    if(buildingId === ""){
        showErrorAlert(getAlertHolder(), "You must choose a building!");
    }
    else if(floorName === ""){
        showErrorAlert(getAlertHolder(), "Floor name must not be empty!");
    }
    else {
        let currentFloors = getCurrentFloors();
        if(currentFloors.includes(floorName)){
            showErrorAlert(getAlertHolder(), `Floor with name '${floorName}' already exists!`);
        } else {
            floorsContainer.prepend(createFloorElement(floorName));
            showSuccessAlert(getAlertHolder(), `Floor '${floorName}' added successfully!`);
        }
    }

    // Remove the No floors sign if it exists
    $("#no_floors").remove()

    floorNameArea.val('');
    $('#add_floor_prompt').modal('hide');
}


function saveFloors(){
    if(buildingId === ""){
        showErrorAlert(getAlertHolder(), "You must choose a building!");
        return;
    }

    $.ajax({
        headers: {'X-CSRFToken' : csrftoken},
        type: 'POST',
        mode: 'same-origin',
        data: {'floors': getCurrentFloors().reverse()},
        url: `/save-building-floors/${buildingId}`,
        success: function(data){
            console.log('Success');
            showSuccessAlert(getAlertHolder(), 'Successfully updated floors!');
        },
        error: function(err){
            console.log('error');
            showErrorAlert(getAlertHolder(), 'An error occurred. Failed to update floors!');
        }
    });
    
}


function createFloorElement(name){
    let randomNum = Math.floor(Math.random() * 10000) + 12345;
    let floorId = "floor_" + name + randomNum;
    return `
        <div id="${floorId}" class="row p-2">
            <div class="h4 col-4 text-center" name="floor">${name}</div>
            <div class="col-8">
                <span class="cursor-pointer" onclick="upArrowClicked('${floorId}')"> <i class="text-primary fas fa-arrow-alt-circle-up fa-2x"></i> </span>
                <span class="cursor-pointer" onclick="downArrowClicked('${floorId}')"> <i class="text-primary fas fa-arrow-alt-circle-down fa-2x"></i> </span>
                <span class="cursor-pointer" onclick="crossClicked('${floorId}')"> <i class="text-danger fas fa-times-circle fa-2x"></i> </span>
            </div>
        </div>
    `;
}

function upArrowClicked() {
    console.log("up clicked");
}

function downArrowClicked() {
    console.log("down clicked");
}

function crossClicked(floorId) {
    $(`#${floorId}`).remove();
}


function getAlertHolder(){
    return $("#alert_holder");
}

function getCurrentFloors(){
    return $("[name='floor']").map(function(){
        return this.innerHTML;
    }).get();
}