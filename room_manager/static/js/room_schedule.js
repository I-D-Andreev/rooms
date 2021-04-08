$(document).ready(function(){
    $('#id_room').on('change', function(){
        let roomId = this.value;
        if(roomId == ""){
            renderMeetingData([]);
        } else {
            $.ajax({
                url: `/get-room-schedule/${roomId}`,
                success: function(data){
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
    meetingsContainer = $('#room_meetings');
    
    // remove child elements
    meetingsContainer.empty();

    if (data.meetings.length > 0){
        for(let i=0; i<data.meetings.length; i++){
            let element = ` 
                <div class="list-group-item border-secondary w-75 mx-auto ${data.meetings[i].background_colour}">
                    <span class="float-left w-25">${data.meetings[i].start_time} - ${data.meetings[i].end_time}</span>
                    <span class="ml-4">${data.meetings[i].name}</span>
                </div>
            `;

            meetingsContainer.append(element)
        }
    }
}
