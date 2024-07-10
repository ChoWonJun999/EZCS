function sendResetRequest() {
    let username = $("#forgotPasswordUsername").val();
    let birthdate = $("#birthdate").val();
    let phone_number = $("#phone_number").val();

    if (!username || !birthdate || !phone_number) {
        alert("모든 필드를 채워주세요.");
        return;
    }

    let data = {
        username: username,
        birthdate: birthdate,
        phone_number: phone_number
    };

    let form = $("#forgotPasswordForm");
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