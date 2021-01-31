$(document).ready(function(){
    $('#id_building').on('change', function(){
        buildingId = this.value;
        if(buildingId == ""){
            renderFloorData(null);
        } else {
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
        $('#floor_name_textarea').focus();
    });
});

function addFloor(){
    console.log('add floor clicked');
}


function saveFloors(){
    console.log('save floors clicked');
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
            <h4> ${name} </h4>
        </div>
    `;
}