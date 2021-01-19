$(document).ready(function(){
    console.log(csrftoken)
    $('#id_meeting').on('change', function(){
        console.log(this.value);
    })
});


function loadMeeting(){

}