$(document).ready(function(){
    const ACCOUNTS = JSON.parse(document.getElementById("accounts").textContent);

    lockReadOnlyFields();

    
    loadAccountsOnTypeChange(ACCOUNTS);
    loadInfoOnAccountChange(ACCOUNTS);
});

function lockReadOnlyFields() {
    $("#id_username").attr("disabled", true);
    $("#id_name").attr("disabled", true);
    $("#id_email").attr("disabled", true);
}

function clearData() {
    $("#id_username").val('');
    $("#id_name").val('');
    $("#id_email").val('');
}

function fillData(data) {
    clearData();

    if(data){
        $("#id_username").val(data.username);
        $("#id_name").val(data.name);
        $("#id_email").val(data.email);
    }
}



function loadAccountsOnTypeChange(ACCOUNTS) {
    let accountsSelect = $("#id_account");

    $("#id_type").on('change', function(){
        clearData();
        
        accountsSelect.empty();
        
        // append empty child
        accountsSelect.append("<option value>---------</option>");
        
        let type = this.value;

        for (let i=0; i<ACCOUNTS[type].length; i++){
            let element = `
                <option value=${ACCOUNTS[type][i].id}>${ACCOUNTS[type][i].name}</option>
            `;
            
            accountsSelect.append(element);
        }
    });
}


function loadInfoOnAccountChange(ACCOUNTS) {
    let accountsSelect = $("#id_account");
    
    accountsSelect.on('change', function(){
        let accountId = this.value;

        if(accountId === ''){
            fillData(null);
        } 
        else {
            let data = null;
            for(let i=0; i<ACCOUNTS.all.length; i++) {
                if(ACCOUNTS.all[i].id == accountId) {
                    data = ACCOUNTS.all[i];
                    break;
                }
            }

            fillData(data);
        }

    });
}