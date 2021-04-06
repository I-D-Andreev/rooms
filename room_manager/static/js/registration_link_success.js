$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();

    $("#copy_icon").on('click', function(){
        console.log($("#register_url").val());
        $("#register_url").select();
        document.execCommand('copy');

        showSuccessAlert($("#alert_holder"), "Copied to clipboard!", delayBeforeFadeMs = 1500);
    });
});