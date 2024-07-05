function resetPassword() {
    let new_password = $("#new_password").val();
    let confirm_password = $("#confirm_password").val();
    let csrf = $("#resetPasswordForm").data("csrf");
    let url = $("#resetPasswordForm").data("url");

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
