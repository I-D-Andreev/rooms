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
});


function renderFloorData(floors_list){
    floors_container = $('#floors');

    // remove child elements
    floors_container.empty();

    if(floors_list !== null){
        if(floors_list.length > 0){
            for(let i=floors_list.length-1; i>=0; i--){
                let element = `
                    <div>
                        <h4> ${floors_list[i].name} </h4>
                    </div>
                `;

                floors_container.append(element);
            }
        }
        else {
            let element = `
            <div>
                <h4> No floors </h4>
            </div>
        `;
            floors_container.append(element);
        }
    }
}