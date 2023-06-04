document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('btn_cancel').addEventListener('click', hideEditForm);
    document.getElementById('btn_edit').addEventListener('click', showEditForm);
	var equipment = document.getElementById('span_equipment').innerHTML;
    if(equipment == "True")
    {
        document.getElementById('span_equipment').innerHTML = 'Yes';
    }
    else if (equipment == "False") {
        document.getElementById('span_equipment').innerHTML = 'No';
    }
    console.log("Span value: " + equipment);
}, false);

function hideEditForm(e) {
    e.preventDefault()
    document.getElementById('edit_form').style.display = 'none';
}

function showEditForm(e) {
    e.preventDefault()
    document.getElementById('edit_form').style.display = 'flex';
}