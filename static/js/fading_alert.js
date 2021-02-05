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

    let tempId = randomNumber(maxNum);

    let element = `
        <div id="${tempId}" class="alert ${alertType} text-center">
            ${alertText}
        </div>
    `;

    alertHolder.append(element);

    $(`#${tempId}`).delay(delayBeforeFadeMs).fadeOut();
}


function randomNumber(maxNum){
    return Math.floor(Math.random() * maxNum);
}