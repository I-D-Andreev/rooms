function showSuccessAlert(alertHolder, alertText, delayBeforeFadeMs = 2500){
    showAlert(alertHolder, alertText, "alert-success", delayBeforeFadeMs);
}

function showErrorAlert(alertHolder, alertText, delayBeforeFadeMs = 2500){
    showAlert(alertHolder, alertText, "alert-danger", delayBeforeFadeMs);
}

function showWarningAlert(alertHolder, alertText, delayBeforeFadeMs=2500){
    showAlert(alertHolder, alertText, "alert-warning", delayBeforeFadeMs);
}

function showAlert(alertHolder, alertText, alertType, delayBeforeFadeMs){
    let maxNum = 5000;
    let fadeOutTime = 2000;

    let tempId = randomNumber(maxNum);

    let element = `
        <div id="${tempId}" class="alert ${alertType} text-center">
            ${alertText}
        </div>
    `;

    alertHolder.append(element);

    $(`#${tempId}`).delay(delayBeforeFadeMs).fadeOut(fadeOutTime, function(){
        $(this).remove();
    });
}


function randomNumber(maxNum){
    return Math.floor(Math.random() * maxNum);
}

function fadePythonMessages(){
    let delayBeforeFadeMs = 2500;

    let messages = $('div.alert');
    for(let i=0; i<messages.length; i++){
        messages.eq(i).delay(delayBeforeFadeMs).fadeOut(2000, function(){
            $(this).remove();
        });
    }
}