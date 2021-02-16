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
            
            // remove pair after modal delete
            $('#confirm_delete').on('hidden.bs.modal', function(){
                let pairDiv = $(`#${building1Id}_${building2Id}_div`);
                pairDiv.remove();

                showSuccessAlert(getAlertHolder(), 'Successfully removed the pair!');

                // detach event listener after the first execution
                $(this).off('hidden.bs.modal');
            });


            // reload the page so the new data can be rendered
            // maybe use this if we also display the inferred pairs
            // might have problems with messages
            // location.reload();
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