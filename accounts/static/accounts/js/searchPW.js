function sendResetRequest() {
    let username = $("#forgotPasswordUsername").val();
    let birthdate = $("#birthdate").val();
    let phone_number = $("#phone_number").val();
    let csrf = $("#showForgotPasswordForm").data("csrf");
    let url = $("#showForgotPasswordForm").data("url");

    $.ajax({
        url: url,
        type: "post",
        data: {
            username: username,
            birthdate: birthdate,
            phone_number: phone_number,
            csrfmiddlewaretoken: csrf
        },
        dataType: "json",
        success: function (data) {
            if (data.result === 'success') {

                alert(data.msg);
                location.href = "/accounts/reset-password/";
            } else {
                alert(data.msg);
            }
        }
    });
}