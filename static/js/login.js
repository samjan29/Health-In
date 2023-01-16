function login() {
    if ($('#login_id').val() == '') {
        return $('#login_id').focus();
    } else if ($('#login_pw').val() == '') {
        return $('#login_pw').focus();
    }

    $.ajax({
        type: "POST",
        url: '/api/login',
        data: {
            'id_give': $('#login_id').val(),
            'pw_give': $('#login_pw').val()
        },
        success: function (response) {
            alert(response['msg']);
            window.location.href = '/';
        }
    });
}

function handleClickJoin() {
    window.location.href = '/login';
}