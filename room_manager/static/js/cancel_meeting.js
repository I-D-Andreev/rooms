$(document).ready(function(){
    $('#id_meeting').on('change', function(){
        meetingId = this.value;
        if(meetingId === ''){
            console.log("empty");
            loadData(null);
        } else {
            $.ajax({
                url: `/get-meeting-creator/${meetingId}`,
                success: function(data){
                    loadData(data);
                    console.log(data);
                },
                error: function(err){
                    console.log(err);
                }
            });
        }
    });

    $('#id_meeting').trigger('change');
});


function loadData(data){
    if(data){
        if(data.account_type !== "room"){
            showHideAuthenticationFields(true);
            $("#id_username").val(data.creator_username);
            // $("#id_password").focus();
        }
        else {
            showHideAuthenticationFields(false);
        }

    } else {
        showHideAuthenticationFields(false);
    }
}

function showHideAuthenticationFields(shouldShow){
    let holder = $("#vis_invis_holder");
    if(shouldShow){
        holder.show();
    } else {
        holder.hide();
    }
}

