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

    // send ajax here


    $('#confirm_delete').on('hidden.bs.modal', function(){
        let pairDiv = $(`#${building1Id}_${building2Id}_div`);
        pairDiv.remove();    
    });

    $('#confirm_delete').modal('hide');
   
}