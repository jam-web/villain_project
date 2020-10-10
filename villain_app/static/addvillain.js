$(document).ready(() => {
    document.getElementById('form').onsubmit = handleAddForm;
});

function handleAddForm(event) {
    event.preventDefault();

    var name = $("input[name='name']").val();
    var description = $("input[name='description']").val();
    var interests = $("input[name='interests']").val();
    var villain_url = $("input[name='url']").val();

    $.post("/add", {
        "name": name,
        "description": description,
        "interests": interests,
        "villain_url": villain_url,
        "date_added": updated_at
    }, function (data) {
        if (data.errors !== undefined) {
            document.getElementById("errors").innerHTML = data.errors.map((error) => (`<div class="error">${error}</div>`)).join("");
        } else {
            window.location = "/";
        }
    })

    return false;
}