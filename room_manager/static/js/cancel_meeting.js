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
    passwordField = $("#id_password")
    if(data){
        if(data.account_type !== "room"){
            showHideAuthenticationFields(true);
            $("#id_username").val(data.creator_username);
            passwordField.val("");
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
    passwordField = $("#id_password")
    
    if(shouldShow){
        holder.show();
        passwordField.prop('required', true);

    } else {
        passwordField.prop('required', false);
        holder.hide();

    }
}

