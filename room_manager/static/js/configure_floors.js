var buildingId = "";

$(document).ready(function(){
    enableButtons(false);

    $('#id_building').on('change', function(){
        buildingId = this.value;

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

    floorNameArea.val('');
    $('#add_floor_prompt').modal('hide');
}


function saveFloors(){
    if(buildingId === ""){
        showErrorAlert(getAlertHolder(), "You must choose a building!");
        return;
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
            <div>
                <h4> No floors </h4>
            </div>
        `;
            floorsContainer.append(element);
        }
    }
}

function createFloorElement(name){
    return `
        <div>
            <h4 name="floor">${name}</h4>
        </div>
    `;
}

function getAlertHolder(){
    return $("#alert_holder");
}

function getCurrentFloors(){
    return $("[name='floor']").map(function(){
        return this.innerHTML;
    }).get();
}