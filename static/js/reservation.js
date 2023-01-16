// 예약 요청 기능
function reserve() {
    const trainer_key = $('#trainer_key').text();
    const member_key = $('#member_key').text();
    const trainer_key_give = parseInt(trainer_key);
    const member_key_give = parseInt(member_key);
    console.log(trainer_key, member_key);
    $.ajax({
        type: "POST",
        url: `api/reservation/member/apply/${trainer_key_give}`,
        hearders: {
            'member_key': member_key_give,
            'trainer_key': trainer_key_give,
        },
        data: {},
        success: function (response) {
            alert(response["msg"])
            window.location.reload()
        }
    });
}