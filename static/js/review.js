function showReviews() {
    const key = 1;
    $.ajax({
        type: "GET",
        url: `/api/trainer/review/${key}`,
        data: {},
        success: function (response) {
            const rows = response['reviewList'];

            // // html 틀짜서 넣기
            // for (let i = 0; i < rows.length; i++) {
            //     // for (let j = 0; j < rows[i]['rank'])
            //     const tempHtml = `<div class="card w-50 mb-3">
            //                         <div class="card-body">
            //                             <h5 class="card-title">${rows[i]['member_name']}</h5>
            //                             <p class="card-text">${rows[i]['content']}</p>
            //                             <span class="star">
            //                                 <img src="../static/image/star.png">
            //                                 <img src="../static/image/star.png">
            //                                 <img src="../static/image/star.png">
            //                                 <img src="../static/image/star.png">
            //                                 <img src="../static/image/star.png">
            //                             </span>
            //                         </div>
            //                     </div>`;
            //
            //     $('#container').append(tempHtml);
            // }
        }
    });
}

function saveReviews() {
    const key = 1;
    const memberKey = 3;
    const rank = 4;
    const content = '운동조아';
    $.ajax({
        type: "POST",
        url: `/api/trainer/review/${key}`,
        data: {
            'member_key_give': memberKey,
            'rank_give': rank,
            'content_give': content
        },
        success: function (response) {
            alert(response['msg']);
        }
    });
}