$(document).ready(function(){
    $('#id_room').on('change', function(){
        roomId = this.value;
        if(roomId == ""){
            renderMeetingData([]);
        } else {
            $.ajax({
                url: `/get-room-schedule/${roomId}`,
                success: function(data){
                    console.log(data);
                    renderMeetingData(data);
                },
                error: function(err){
                    console.log(err);
                }
            });
        }
    });
});


function renderMeetingData(data){
    meetings_container = $('#room_meetings');
    
    // remove child elements
    meetings_container.empty();

    if (data.length > 0){
        for(let i=0; i<data.length; i++){
            let element = ` 
                <div class="list-group-item border-secondary w-75 mx-auto ${data[i].background_colour}">
                    <span class="float-left w-25">${data[i].start_time} - ${data[i].end_time}</span>
                    <span class="ml-4">${data[i].name}</span>
                </div>
            `;

            meetings_container.append(element)
        }
    }
}
