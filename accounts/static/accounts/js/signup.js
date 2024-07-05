function signup() {
    let username = $("#loginUsername").val();
    let name = $("#name").val();
    let phone = $("#phone").val();

    if (containsKorean(username)) {
        $("#usernameError").text("아이디는 한글을 포함할 수 없습니다.");
        $("#usernameError").show();
        return false;
    } else {
        $("#usernameError").hide();
    }

    if (!isKorean(name)) {
        $("#nameError").text("이름은 한글만 포함해야 합니다.");
        $("#nameError").show();
        return false;
    } else {
        $("#nameError").hide();
    }

    
    let password = $("#password").val();
    let password_confirm = $("#pwChk").val();

    if (password != password_confirm) {
        alert("비밀번호가 일치하지 않습니다.");
        return false;
    }
    if (!validatePassword(password)) {
        $("#passwordError").text("비밀번호는 최소 8자 이상이어야 하며, 대문자, 소문자, 숫자, 특수문자를 포함해야 합니다.");
        $("#passwordError").show();
        return false;
    } else {
        $("#passwordError").hide();
    }


    if (password !== password_confirm) {
        $("#passwordConfirmError").text("비밀번호가 일치하지 않습니다.");
        $("#passwordConfirmError").show();
        return false;
    } else {
        $("#passwordConfirmError").hide();
    }

    $("#addressCode").removeAttr("disabled");


    let email = $("#email").val();
    let emailDomain = $("#emailadd").val();
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
        username: username,
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

$(document).ready(function () {
    if (window.location.pathname === '/accounts/signup/'){
        $("#loginUsername").on("input", function () {
            let username = $(this).val();
            let csrf = $("#signupForm").data("csrf");

            $.ajax({
                url: "/accounts/check-username/",
                type: "get",
                data: { username: username },
                dataType: "json",
                headers: {
                    "X-CSRFToken": csrf
                },
                success: function (data) {
                    if (data.is_taken) {
                        $("#usernameError").text("이미 가입된 아이디입니다.");
                        $("#usernameError").show();
                        $("#loginUsername").addClass("is-invalid");
                    } else {
                        $("#usernameError").hide();
                        $("#loginUsername").removeClass("is-invalid");
                    }
                }
            });
        });

        $("#email").on("input", function () {
            let email = $(this).val();
            let csrf = $("#signupForm").data("csrf");

            $.ajax({
                url: "/accounts/check-email/",
                type: "get",
                data: { email: email + "@" + $("#emailadd").val() },
                dataType: "json",
                headers: {
                    "X-CSRFToken": csrf
                },
                success: function (data) {
                    if (data.is_taken) {
                        $("#emailError").text("이미 가입된 이메일입니다.");
                        $("#emailError").show();
                        $("#email").addClass("is-invalid");
                    } else {
                        $("#emailError").hide();
                        $("#email").removeClass("is-invalid");
                    }
                }
            });
        });
        
        $("#phone").on("input", function () {
            let phone = $(this).val();
            let csrf = $("#signupForm").data("csrf");

            $.ajax({
                url: "/accounts/check-phone/",
                type: "get",
                data: { phone_number: phone },
                dataType: "json",
                headers: {
                    "X-CSRFToken": csrf
                },
                success: function (data) {
                    if (data.is_taken) {
                        $("#phoneError").text("이미 가입된 전화번호입니다.");
                        $("#phoneError").show();
                        $("#phone").addClass("is-invalid");
                    } else {
                        $("#phoneError").hide();
                        $("#phone").removeClass("is-invalid");
                    }
                }
            });
        });
    }
    $("#UserAdd2").on("input", function () {
        let addressDetail = $(this).val();
        if (addressDetail) {
            $("#userAdd2Error").hide();
        }
    });
});


function isKorean(text) {
    var koreanRegex = /^[가-힣]+$/;
    return koreanRegex.test(text);
}

function containsKorean(text) {
    var koreanRegex = /[ㄱ-ㅎㅏ-ㅣ가-힣]/;
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
