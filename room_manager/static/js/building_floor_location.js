function loadFloorsOnBuildingChange(buildingSelect, floorsSelect){
    buildingSelect.on('change', function(){
        let currentId = this.value
        let url = currentId ? `/get-building-floors/${currentId}` : '/get-building-floors';

        $.ajax({
            url: url,
            success: function(data){
                loadDataInSecondSelect(floorsSelect, data);         
            },
            error: function(err){
                console.log(err);
            }
        });
    });
}

function loadDataInSecondSelect(floorsSelect, data){
    // clear children
    floorsSelect.empty();

    // append empty child
    floorsSelect.append("<option value></option>");

    for(let i=0; i<data.length; i++){
        let element = `
            <option value=${data[i].id}>${data[i].full_name}</option>
        `;
        floorsSelect.append(element);
    }
}
