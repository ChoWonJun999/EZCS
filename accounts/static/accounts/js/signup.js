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

    if (!isAlphanumeric(username.val())) {
        $("#usernameError").text("아이디는 영어와 숫자만 포함할 수 있습니다.");
        $("#usernameError").show();
        username.addClass("is-invalid");
        username.focus();
        return;
    } else {
        $("#usernameError").hide();
        username.removeClass("is-invalid");
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
                username.removeClass("is-invalid");
                username.addClass("is-valid");
                $("#usernameChk").val(username.val());
            }
        }
    });
}

function checkKoreanName(obj) {
    if (obj.value.trim() == "") {
        $("#nameError").text("이름을 입력해 주세요.");
        $("#nameError").show();
        obj.classList.add("is-invalid");
        if (obj.classList.contains("is-valid")) {
            obj.classList.remove("is-valid");
        }
    } else if (!isKorean(obj.value)) { 
        $("#nameError").text("이름은 한글만 포함해야 합니다.");
        $("#nameError").show();
        obj.classList.add("is-invalid");
        if (obj.classList.contains("is-valid")) {
            obj.classList.remove("is-valid");
        }
    } else {
        $("#nameError").hide();
        obj.classList.remove("is-invalid");
        obj.classList.add("is-valid");
    }
}

function chkPhoneNumber() {
    let phone = $("#phone").val();
    if (phone.trim() == "") { 
        $("#phoneError").text("핸드폰 번호를 입력하세요.");
        $("#phoneError").show();
        $("#phone").addClass("is-invalid");
        return false;
    } else if (!/^\d+$/.test(phone)) { 
        $("#phoneError").text("입력 형식은 숫자만 입력해주세요.");
        $("#phoneError").show();
        $("#phone").addClass("is-invalid");
        return false;
    } else if (!phone.startsWith("010")) {
        $("#phoneError").text("핸드폰 번호는 010으로 시작해야 합니다.");
        $("#phoneError").show();
        $("#phone").addClass("is-invalid");
        return false;
    } else if (phone.length !== 11) {
        $("#phoneError").text("핸드폰 번호는 11자리여야 합니다.");
        $("#phoneError").show();
        $("#phone").addClass("is-invalid");
        return false;
    } else {
        $("#phoneError").hide();
        $("#phone").removeClass("is-invalid");
        $("#phone").addClass("is-valid");
    }

    $.ajax({
        url: $("#phoneChkUrl").val(),
        type: "get",
        data: { phone_number: phone },
        dataType: "json",
        headers: {
            "X-CSRFToken": $("#csrf").val()
        },
        success: function (data) {
            $("#phoneError").hide();
            $("#phone").removeClass("is-invalid");
            $("#phone").addClass("is-valid");
        }
    });
}

function chkEmail() {
    let emailLocal = $("#emailLocal").val();
    let emailDomain = $("#emailDomain").val();
    let email = emailLocal + "@" + emailDomain;

    if (emailLocal.trim() == "") {
        $("#emailError").text("이메일을 입력하세요.");
        $("#emailError").show();
        $("#emailLocal").addClass("is-invalid");
        return false;
    } else if (!isAlphanumeric(emailLocal)) {
        $("#emailError").text("이메일은 영어와 숫자만 포함할 수 있습니다.");
        $("#emailError").show();
        $("#emailLocal").addClass("is-invalid");
        return false;
    } else {
        $("#emailError").hide();
        $("#emailLocal").removeClass("is-invalid");
        $("#emailLocal").addClass("is-valid");
    }

    $.ajax({
        url: $("#emailChkUrl").val(),
        type: "get",
        data: { email: email },
        dataType: "json",
        headers: {
            "X-CSRFToken": $("#csrf").val()
        },
        success: function (data) {
            if (data.is_taken) {
                $("#emailError").text("이미 가입된 이메일입니다.");
                $("#emailError").show();
                $("#emailLocal").addClass("is-invalid");
            } else {
                $("#emailError").hide();
                $("#emailLocal").removeClass("is-invalid");
                $("#emailLocal").addClass("is-valid");
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
    let password = $("#password").val().toLowerCase();
    let password_confirm = $("#pwChk").val().toLowerCase();

    if (password.length < 8 || !/\W/.test(password)) {
        $("#passwordError").text("비밀번호는 8자리 이상이어야 하며, 특수문자를 포함해야 합니다.");
        $("#passwordError").show();
        $("#password").addClass("is-invalid");
    } else if (password !== password_confirm) {
        $("#passwordError").text("비밀번호가 다릅니다.");
        $("#passwordError").show();
        $("#pwChk").addClass("is-invalid");
    } else {
        $("#passwordError").hide();
        $("#password").removeClass("is-invalid");
        $("#password").addClass("is-valid");
        $("#pwChk").removeClass("is-invalid");
        $("#pwChk").addClass("is-valid");
    }
}

function chkAddressDetail() {
    let addressDetail = $("#UserAdd2").val();
    if (!addressDetail) {
        $("#userAdd2Error").text("상세 주소를 입력해 주세요.");
        $("#userAdd2Error").show();
        $("#UserAdd2").addClass("is-invalid");
        return false;
    } else {
        $("#userAdd2Error").hide();
        $("#UserAdd2").removeClass("is-invalid");
        $("#UserAdd2").addClass("is-valid");
    }
}

function chkBirthdate() {
    let birthdate = $("#birthdate").val();
    if (birthdate.trim() == "") {
        $("#birthdateError").text("생년월일을 입력해 주세요.");
        $("#birthdateError").show();
        $("#birthdate").addClass("is-invalid");
        return false;
    } else {
        $("#birthdateError").hide();
        $("#birthdate").removeClass("is-invalid");
        $("#birthdate").addClass("is-valid");
        return true;
    }
}

function signup() {
    let username = $("#loginUsername");
    let name = $("#name").val();
    let phone = $("#phone").val();
    let valid = true;

    if (username.val().trim() == "") {
        $("#usernameError").text("아이디를 입력하세요.");
        $("#usernameError").show();
        username.addClass("is-invalid");
        if (username.hasClass("is-valid")) {
            username.removeClass("is-valid");
        }
        username.focus();
        valid = false;
    } else if (containsKorean(username.val()) || !isAlphanumeric(username.val())) {
        $("#usernameError").text("아이디는 영어와 숫자만 포함할 수 있습니다.");
        $("#usernameError").show();
        username.addClass("is-invalid");
        username.focus();
        valid = false;
    }

    if ("" == $("#usernameChk").val()) {
        $("#usernameError").text("아이디 중복 확인을 하세요.");
        $("#usernameError").show();
        $("#usernameVaild").hide();
        username.addClass("is-invalid");
        if (username.hasClass("is-valid")) {
            username.removeClass("is-valid");
        }
        username.focus();
        valid = false;
    }

    if (name.trim() == "") {
        $("#nameError").text("이름을 입력해 주세요.");
        $("#nameError").show();
        $("#name").addClass("is-invalid");
        $("#name").focus();
        valid = false;
    } else if (!isKorean(name)) {
        $("#nameError").text("이름은 한글만 포함해야 합니다.");
        $("#nameError").show();
        $("#name").addClass("is-invalid");
        $("#name").focus();
        valid = false;
    } else {
        $("#nameError").hide();
        $("#name").removeClass("is-invalid");
        $("#name").addClass("is-valid");
    }

    if (phone.trim() == "") { 
        $("#phoneError").text("핸드폰 번호를 입력하세요.");
        $("#phoneError").show();
        $("#phone").addClass("is-invalid");
        $("#phone").focus();
        valid = false;
    } else if (!/^\d+$/.test(phone)) {
        $("#phoneError").text("입력 형식은 숫자만 입력해주세요.");
        $("#phoneError").show();
        $("#phone").addClass("is-invalid");
        $("#phone").focus();
        valid = false;
    } else if (!phone.startsWith("010")) { 
        $("#phoneError").text("핸드폰 번호는 010으로 시작해야 합니다.");
        $("#phoneError").show();
        $("#phone").addClass("is-invalid");
        $("#phone").focus();
        valid = false;
    } else if (phone.length !== 11) { 
        $("#phoneError").text("핸드폰 번호는 11자리여야 합니다.");
        $("#phoneError").show();
        $("#phone").addClass("is-invalid");
        $("#phone").focus();
        valid = false;
    } else {
        $("#phoneError").hide();
        $("#phone").removeClass("is-invalid");
        $("#phone").addClass("is-valid");
    }

    let password = $("#password").val().toLowerCase();
    let password_confirm = $("#pwChk").val().toLowerCase();

    if (password.length < 8 || !/\W/.test(password)) { 
        $("#passwordError").text("비밀번호는 8자리 이상이어야 하며, 특수문자를 포함해야 합니다.");
        $("#passwordError").show();
        $("#password").addClass("is-invalid");
        $("#password").focus();
        valid = false;
    } else if (password != password_confirm) {
        $("#passwordError").text("비밀번호가 일치하지 않습니다.");
        $("#passwordError").show();
        $("#pwChk").focus();
        valid = false;
    } else {
        $("#passwordError").hide();
    }

    let emailLocal = $("#emailLocal").val();
    let emailDomain = $("#emailDomain").val();
    let fullEmail = emailLocal + "@" + emailDomain;

    if (emailLocal.trim() == "") {
        $("#emailError").text("이메일을 입력하세요.");
        $("#emailError").show();
        $("#emailLocal").addClass("is-invalid");
        $("#emailLocal").focus();
        valid = false;
    } else if (!isAlphanumeric(emailLocal)) {
        $("#emailError").text("이메일은 영어와 숫자만 포함할 수 있습니다.");
        $("#emailError").show();
        $("#emailLocal").addClass("is-invalid");
        $("#emailLocal").focus();
        valid = false;
    } else {
        $("#emailError").hide();
        $("#emailLocal").removeClass("is-invalid");
        $("#emailLocal").addClass("is-valid");
    }

    if (!valid) {
        return;
    }
    if (!chkBirthdate()) {
        valid = false;
    }

   
    let addressDetail = $("#UserAdd2").val();
    if (!addressDetail) {
        $("#userAdd2Error").text("상세 주소를 입력해 주세요.");
        $("#userAdd2Error").show();
        $("#UserAdd2").focus();
        valid = false;
    } else {
        $("#userAdd2Error").hide();
    }

    if (!valid) {
        return;
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
    var koreanRegex = /[ㄱ-ㅎㅏ-ㅣ가-힣]/;
    return koreanRegex.test(text);
}

function isAlphanumeric(text) {
    var alphanumericRegex = /^[a-zA-Z0-9]+$/;
    return alphanumericRegex.test(text);
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