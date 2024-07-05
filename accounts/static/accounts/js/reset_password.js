function validatePassword(password) {
    var passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return passwordRegex.test(password);
}

function resetPassword() {
    let new_password = $("#new_password").val();
    let confirm_password = $("#confirm_password").val();
    let csrf = $("input[name='csrfmiddlewaretoken']").val();
    let url = $("#resetPasswordForm").data("url");

    if (!validatePassword(new_password)) {
        alert("비밀번호는 최소 8자 이상이어야 하며, 대문자, 소문자, 숫자, 특수문자를 포함해야 합니다.");
        return;
    }
    if (new_password !== confirm_password) {
        alert("비밀번호가 일치하지 않습니다.");
        return;
    }

    $.ajax({
        url: url,
        type: "post",
        data: {
            new_password: new_password,
            csrfmiddlewaretoken: csrf
        },
        dataType: "json",
        success: function (data) {
            if (data.result === 'success') {
                alert(data.msg);
                location.href = "/accounts/";
            } else {
                alert(data.msg);
            }
        }
    });
}
