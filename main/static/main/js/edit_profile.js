function validatePassword(password) {
    var passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return passwordRegex.test(password);
}

function submitProfile() {
    let name = $("#name").val();
    let email = $("#email").val();
    let phone_number = $("#phone_number").val();
    let birth_date = $("#birth_date").val();
    let address_code = $("#address_code").val();
    let address = $("#address").val();
    let address_detail = $("#address_detail").val();
    let password = $("#password").val();
    let password_confirm = $("#password_confirm").val();

    if (password !== password_confirm) {
        alert("비밀번호가 일치하지 않습니다.");
        return false;
    }

    if (password && !validatePassword(password)) {
        alert("비밀번호는 최소 8자 이상이어야 하며, 대문자, 소문자, 숫자, 특수문자를 포함해야 합니다.");
        return false;
    }

    let param = {
        name: name,
        email: email,
        phone_number: phone_number,
        birth_date: birth_date,
        address_code: address_code,
        address: address,
        address_detail: address_detail,
        password: password
    };

    var from = $("#editProfileForm");
    var url = from.data("url");
    var csrf = from.data("csrf");

    $.ajax({
        url: url,
        type: "post",
        data: param,
        dataType: "json",
        headers: {
            "X-CSRFToken": csrf
        },
        success: function (data) {
            if (data.result) {
                alert(data.msg);
                location.href = "/";
            } else {
                alert(data.msg);
            }
        }
    });
}

$(document).ready(function () {
    $("#birth_date").val(new Date($("#birth_date").val()).toISOString().slice(0, 10));
});
