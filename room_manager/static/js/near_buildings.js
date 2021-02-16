$(document).ready(function(){
    fadePythonMessages();
})


function crossClicked(building1Id, building2Id){
    console.log(building1Id);
    console.log(building2Id);

    let divId = `${building1Id}_${building2Id}`;
    console.log(divId);
    // $(`#${divId}`).remove();

}