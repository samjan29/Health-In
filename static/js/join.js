function signup() {
    if ($('#id > input').val() == '') {
        return $('#id > input').focus();
    } else if ($('#pw').val() == '') {
        return $('#pw').focus();
    } else if ($('#pw2').val() == '') {
        return $('#pw2').focus();
    } else if ($('#nickname').val() == '') {
        return $('#nickname').focus();
    } else if ($('input:radio[name=flexRadioDefault]:radio:checked').length < 1) {
        return alert('회원 타입을 선택해주세요!');
    }

    const role = $('input:radio[name=flexRadioDefault]:checked').val();

    $.ajax({
        type: "POST",
        url: '/api/join',
        data: {
            'id_give': $('#id  > input').val(),
            'pw_give': $('#pw').val(),
            'nickname_give': $('#nickname').val(),
            'role_give': role
        },
        success: function (response) {
            alert(response['msg']);
            window.location.href = '/login';
        }
    });
}