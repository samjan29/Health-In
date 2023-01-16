

function trainer_check() {
    $.ajax({
        type: "GET",
        url: "/api/trainer/check_list",
        data: {},
        success: function (response) {
            let rows = response['trainer_list']
            for (let i = 0; i < rows.length; i++) {
                let key = rows[i]['key']
                let trainer_id = rows[i]['trainer_id']
                let password = rows[i]['password']
                let role = rows[i]['role']
                let image = rows[i]['image']
                let name = rows[i]['name']
                let region = rows[i]['region']
                let category = rows[i]['category']
                let timetable = rows[i]['timetable']
                let price = rows[i]['price']
                let description = rows[i]['description']


                $('#category').val(category)
                $('#name').val(name)
                $('#region').val(region)
                $('#timetable').val(timetable)
                $('#price').val(price)
                $('#description').val(description)
            }
        }
    })
}
function trainer(name){
    $.ajax({
        type: "POST",
        url: "/api/trainer/check",
        data: {name_give:name},
        success:function(response){
        alert(response['msg'])
        window.location.reload()
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