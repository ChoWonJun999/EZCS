function sendResetRequest() {
    let username = $("#forgotPasswordUsername").val();
    let birthdate = $("#birthdate").val();
    let phone_number = $("#phone_number").val();
    let csrf = $("#showForgotPasswordForm").data("csrf");
    let url = $("#showForgotPasswordForm").data("url");

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
                window.location.href = "/accounts/reset_password/";
            } else {
                alert(response.msg);
            }
        }
    });
}

function chkUserName() {
    let username = $("#forgotPasswordUsername");
    let name = $("#name").val();
    let phone = $("#phone").val();

    if (username.val().trim() == "") {
        $("#usernameError").text("아이디를 입력하세요.");
        $("#usernameError").show();
        username.addClass("is-invalid");
        if (username.hasClass("is-valid")) {
            username.removeClass("is-valid");
        }
        username.focus();
        return;
    }
}