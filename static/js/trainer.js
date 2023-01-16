$(document).ready(function () {
    trainer_check();
});

function trainer_check() {
    $.ajax({
        type: "GET",
        url: "/api/trainer/check",
        data: {},
        success: function (response) {
            let rows = response['trainer_list']
            console.log(rows)

        }

    })
}
function trainer_register() {
    let image = $('#image').val()
    let name = $('#name').val()
    let region = $('#region').val()
    let category = $('#category').val()
    let timetable = $('#timetable').val()
    let price = $('#price').val()
    let description = $('#description').val()

    $.ajax({
        type: "POST",
        url: "/api/trainer/register",
        data: {
            name_give: name,
            region_give: region,
            category_give: category,
            timetable_give: timetable,
            price_give: price,
            description_give: description
        },

        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }

    })
}