function resetPassword() {
    let new_password = $("#new_password").val();
    let confirm_password = $("#confirm_password").val();

    if (!new_password || !confirm_password) {
        alert("모든 필드를 채워주세요.");
        return;
    }

    if (new_password !== confirm_password) {
        alert("비밀번호가 일치하지 않습니다.");
        return;
    }

    let data = {
        new_password: new_password
    };

    let form = $("#resetPasswordForm");
    let url = form.data("url");
    let csrf = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
        url: url,
        type: "post",
        data: data,
        dataType: "json",
        headers: {
            "X-CSRFToken": csrf
        },
        success: function (response) {
            if (response.result === 'success') {
                alert(response.msg);
                window.location.href = "/accounts/";
            } else {
                alert(response.msg);
            }
        }
    });
}
