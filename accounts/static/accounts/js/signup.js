function nameChange(obj) {
    if (obj.value != $("#usernameChk").val()) {
        $("#usernameVaild").hide();
        $("#usernameError").hide();
        if (obj.classList.contains("is-invalid")) {
            obj.classList.remove("is-invalid");
        }
        if (obj.classList.contains("is-valid")) {
            obj.classList.remove("is-valid");
        }
        $("#usernameChk").val("");
    }
}

function chkUserName() {
    let username = $("#loginUsername");

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

    if (containsKorean(username)) {
        $("#usernameError").text("아이디는 한글을 포함할 수 없습니다.");
        $("#usernameError").show();
        return;
    } else {
        $("#usernameError").hide();
    }

    $.ajax({
        url: $("#usernameChkUrl").val(),
        type: "post",
        data: { username: username.val() },
        dataType: "json",
        headers: {
            "X-CSRFToken": $("#csrf").val()
        },
        success: function (data) {
            if (data.is_taken) {
                $("#usernameError").text("이미 가입된 아이디입니다.");
                $("#usernameError").show();
                $("#usernameVaild").hide();
                username.addClass("is-invalid");
                if (username.hasClass("is-valid")) {
                    username.removeClass("is-valid");
                }
                username.focus();
                $("#usernameChk").val("");
            } else {
                $("#usernameVaild").text("사용 가능한 아이디입니다.");
                $("#usernameVaild").show();
                $("#usernameError").hide();
                if (username.hasClass("is-invalid")) {
                    username.removeClass("is-invalid");
                }
                username.addClass("is-valid");
                $("#usernameChk").val(username.val());
            }
        }
    });
}

function emailDomainChange(obj) {
    $("#emailDomain").val(obj.value);
    if (obj.value == "") {
        $("#emailDomain").attr("disabled", false);
    } else {
        $("#emailDomain").attr("disabled", true);
    }
}

function pwBlur() {
    if ($("#password").val() != $("#pwChk").val()) {
        $("#passwordError").text("비밀번호가 다릅니다.");
        $("#passwordError").show();
        $("#pwChk").addClass("is-invalid");
        $("#pwChk").focus();
    } else {
        $("#passwordError").hide();
        if ($("#pwChk").hasClass("is-invalid")) {
            $("#pwChk").removeClass("is-invalid");
        }
    }
}

function signup() {
    let username = $("#loginUsername");
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

    if ("" == $("#usernameChk").val()) {
        $("#usernameError").text("아이디 중복 확인을 하세요.");
        $("#usernameError").show();
        $("#usernameVaild").hide();
        username.addClass("is-invalid");
        if (username.hasClass("is-valid")) {
            username.removeClass("is-valid");
        }

        // ERROR focus 안잡힘
        //username.focus();
        return;
    }

    if (!isKorean(name)) {
        $("#nameError").text("이름은 한글만 포함해야 합니다.");
        $("#nameError").show();
        return false;
    } else {
        $("#nameError").hide();
    }

    let password = $("#password").val().toLowerCase();
    let password_confirm = $("#pwChk").val().toLowerCase();

    if (password != password_confirm) {
        alert("비밀번호가 일치하지 않습니다.");
        return false;
    }

    // if (!validatePassword(password)) {
    //     $("#passwordError").text("비밀번호는 최소 8자 이상이어야 하며, 문자, 숫자, 특수문자를 포함해야 합니다.");
    //     $("#passwordError").show();
    //     return false;
    // } else {
    //     $("#passwordError").hide();
    // }

    if (password !== password_confirm) {
        $("#passwordConfirmError").text("비밀번호가 일치하지 않습니다.");
        $("#passwordConfirmError").show();
        return false;
    } else {
        $("#passwordConfirmError").hide();
    }

    let email = $("#emailLocal").val();
    let emailDomain = $("#emailDomain").val();
    if (!email || !emailDomain) {
        $("#emailError").text("이메일을 입력해 주세요.");
        $("#emailError").show();
        return false;
    } else {
        $("#emailError").hide();
    }

    let fullEmail = email + "@" + emailDomain;
    let addressDetail = $("#UserAdd2").val();
    if (!addressDetail) {
        $("#userAdd2Error").text("상세 주소를 입력해 주세요.");
        $("#userAdd2Error").show();
        return false;
    } else {
        $("#userAdd2Error").hide();
    }
    let param = {
        username: username.val(),
        password: password,
        name: name,
        phone_number: phone,
        email: fullEmail,
        birthdate: $("#birthdate").val(),
        addressCode: $("#addressCode").val(),
        address: $("#UserAdd1").val(),
        addressDetail: addressDetail
    };

    var from = $("#signupForm");
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
            $("#addressCode").attr("disabled", true);
            if (data.result) {
                alert(data.msg);
                location.href = "/accounts";
            } else {
                alert(data.msg);
            }
        }
    });
}

function isKorean(text) {
    var koreanRegex = /^[가-힣]+$/;
    return koreanRegex.test(text);
}

function containsKorean(text) {
    var koreanRegex = /^[A-Za-z0-9]+$/;
    return koreanRegex.test(text);
}

function validatePassword(password) {
    var passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return passwordRegex.test(password);
}

function displayErrors(errors) {
    for (let key in errors) {
        let errorDiv = $("#" + key + "Error");
        errorDiv.text(errors[key]);
        errorDiv.show();
    }
}

function toggleDropdown() {
    var dropdown = document.getElementById("emailDropdown");
    dropdown.toggleClass("show");
}

function setEmailDomain(domain) {
    $("#emailadd").val(domain);
    toggleDropdown();
}

function enableDirectInput() {
    $("#emailadd").val("");
    $("#emailadd").attr("readonly");
    $("#emailadd").css("background-color", "#fff");
    $("#emailadd").css("color", "#000");
    $("#emailadd").focus();
    toggleDropdown();
}

function execDaumPostcode() {
    new daum.Postcode({
        oncomplete: function (data) {
            var addr = "";
            var extraAddr = "";

            if (data.userSelectedType === "R") {
                addr = data.roadAddress;
            } else {
                addr = data.jibunAddress;
            }

            if (data.userSelectedType === "R") {
                if (data.bname !== "" && /[동|로|가]$/g.test(data.bname)) {
                    extraAddr += data.bname;
                }
                if (data.buildingName !== "" && data.apartment === "Y") {
                    extraAddr += extraAddr !== "" ? ", " + data.buildingName : data.buildingName;
                }
                if (extraAddr !== "") {
                    extraAddr = " (" + extraAddr + ")";
                }
            }

            document.getElementById("addressCode").value = data.zonecode;
            document.getElementById("UserAdd1").value = addr;
            document.getElementById("UserAdd1").value += extraAddr;
            document.getElementById("UserAdd2").focus();
        }
    }).open();
}
