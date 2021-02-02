function showSuccessAlert(alertHolder, alertText){
    showAlert(alertHolder, alertText, true);
}

function showErrorAlert(alertHolder, alertText){
    showAlert(alertHolder, alertText, false);
}

function showAlert(alertHolder, alertText, isSuccess){
    let maxNum = 5000;
    let delayBeforeFade = 3000; // ms

    let alertType = isSuccess ? "alert-success" : "alert-danger";
    let tempId = randomNumber(maxNum);

    let element = `
        <div id="${tempId}" class="alert ${alertType} text-center">
            ${alertText}
        </div>
    `;

    alertHolder.append(element);

    $(`#${tempId}`).delay(delayBeforeFade).fadeOut();
}


function randomNumber(maxNum){
    return Math.floor(Math.random() * maxNum);
}