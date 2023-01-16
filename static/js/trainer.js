$(document).ready(function () {
    //전체조회
    trainer_check();
});

// 트레이너 조회
function trainer_check() {
    $.ajax({
        type: "GET",
        url: "/api/trainer/check",
        data: {},
        success: function (response) {
            let rows = response['trainer_list'];

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

                console.log(name)

                let temp_html = ``;
                 temp_html=`
                    <div class="box">
                        <div class="contents">
                            <img id="image" src="https://cdnweb01.wikitree.co.kr/webdata/editor/202103/04/img_20210304141854_d90cf7d5.webp"
                                 alt="이미지">
                            <div class="content">
                                <input id="name" type="text" class="form-control submit-text info" value="${name}">
                                <input id="category" type="text" class="form-control submit-text info" value="${category}">
                                <input id="region" type="text" class="form-control submit-text info" value="${region}">
                                <input id="timetable" type="text" class="form-control submit-text info" value="${timetable}">
                                <input id="price" type="text" class="form-control submit-text info" value="${price}">
                            </div>
                        </div>         
                `;
                $('#warp').append(temp_html);
            }

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