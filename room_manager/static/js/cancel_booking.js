$(document).ready(function(){
    $('#id_meeting').on('change', function(){
        let mId = this.value;

        if (mId === "") {
            console.log('empty');
            loadMeeting('', '', '', '', '');
        }
        else {
            $.ajax({
                url: `/get-meeting/${mId}`,
                success: function(data){
                    loadMeeting(data.room, data.start_date, data.start_time, data.duration, data.participants_count);
                },
                error: function(err){
                    console.log(err);
                }
            });
        }
    })
});


function loadMeeting(room, start_date, start_time, duration, participants_count){
    $('#id_room').val(room); 
    $('#id_start_date').val(start_date); 
    $('#id_start_time').val(start_time);
    $('#id_duration').val(duration);
    $('#id_participants_count').val(participants_count);
}