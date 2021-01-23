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
    })
});


function renderMeetingData(data){
    meetings_container = $('#room_meetings');
    
    // remove child elements
    meetings_container.empty()

    if (data.length > 0){
        for(let i=0; i<data.length; i++){
            let backgroundColour = data[i].fields.creator ? 'bg-light-red' : 'bg-green';
            let element = ` 
                <div class="list-group-item border-secondary ${backgroundColour}">
                    <span class="float-left w-25">${data[i].fields.start_time}</span>
                    <span class="ml-4">${data[i].fields.name}</span>
                </div>
            `;

            meetings_container.append(element)
        }
    }
}
