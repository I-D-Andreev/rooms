var lastBuilding1 = null;
var lastBuilding2 = null;

$(document).ready(function(){
    $("#delete_pair").on('click', deletePair);
    fadePythonMessages();
});


function crossClicked(building1Id, building2Id){
    triggerConfirmDialog(building1Id, building2Id);
}

function triggerConfirmDialog(building1Id, building2Id){
    let pairName = $(`#${building1Id}_${building2Id}_pair`).text();
    let confirmDeleteText = pairName ? `Do you want to delete pair "${pairName}"?` : "Do you want to delete the pair?";

    lastBuilding1 = building1Id;
    lastBuilding2 = building2Id;
 
    $('#confirm_delete_text').text(confirmDeleteText);
    $('#confirm_delete').modal('show');
}

function deletePair(){
    let building1Id = lastBuilding1;
    let building2Id = lastBuilding2;

    $.ajax({
        headers: {'X-CSRFToken' : csrftoken},
        type: 'DELETE',
        mode: 'same-origin',
        url: `/near-buildings-pair/${building1Id}/${building2Id}`,
        success: function(data){
            console.log(data);

            // remove pair after modal disappears
            $('#confirm_delete').on('hidden.bs.modal', function(){
                let pairDiv = $(`#${building1Id}_${building2Id}_div`);
                pairDiv.remove();
                
                // remove all inferred pairs
                $("[name='inferred']").remove();

                // re-add the newly calculated inferred pairs
                for(let i=0; i<data.length; i++){
                    $("#pairs_holder").append(createInferredElement(data[i].building1_name, data[i].building2_name));
                }

                showSuccessAlert(getAlertHolder(), 'Successfully removed the pair!');

                // detach event listener after the first execution
                $(this).off('hidden.bs.modal');
            });
        },
        error: function(err){
            console.log(err);
            showErrorAlert(getAlertHolder(), 'An error occurred. Failed to remove the pair!');
        }
    })

    $('#confirm_delete').modal('hide');
   
}

function getAlertHolder(){
    return $("#alert_holder");
}

function createInferredElement(building1Name, building2Name){
    let element = `
    <div class="text-center p-2" name="inferred">
        <span class="h5 text-dark font-weight-bold">${building1Name} - ${building2Name}</span>
        <span class="ml-2 font-italic">(inferred)</span>
    </div>
    `;

    return element;
}