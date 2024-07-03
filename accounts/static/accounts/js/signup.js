function signup() {
    let username = $("#loginUsername").val();
    let name = $("#name").val();

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
    let param = {
        username: $("#loginUsername").val(),
        password: $("#password").val(),
        password_confirm: $("#pwChk").val(),
        name: $("#name").val(),
        email: $("#email").val() + "@" + $("#emailadd").val(),
        birthdate: $("#birthdate").val(),
        zipp_code: $("#zipp_code_id").val(),
        user_add1: $("#UserAdd1").val(),
        user_add2: $("#UserAdd2").val(),
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
            if (data.success) {
                alert("회원가입 요청이 완료되었습니다.");
                location.href = "/accounts";
            } else {
                // errors 키를 통해 각 필드별 오류 메시지를 출력
                //for (let key in data.errors) {
                //    alert(data.errors[key]);
                // 추가 displayErrors
                    displayErrors(data.errors);
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

function displayErrors(errors) {
    for (let key in errors) {
        let errorDiv = $("#" + key + "Error");
        errorDiv.text(errors[key]);
        errorDiv.show();
    }
}


function toggleDropdown() {
    var dropdown = document.getElementById("emailDropdown");
    dropdown.classList.toggle("show");
}

function setEmailDomain(domain) {
    $("#emailadd").val(domain);
}

function enableDirectInput() {
    $("#emailadd").val("");
    $("#emailadd").attr("readonly", false);
    $("#emailadd").css("background-color", "#fff");
    $("#emailadd").css("font-family", "#000");
    $("#emailadd").focus();
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

            document.getElementById("zipp_code_id").value = data.zonecode;
            document.getElementById("UserAdd1").value = addr;
            document.getElementById("UserAdd1").value += extraAddr;
            document.getElementById("UserAdd2").focus();
        }
    }).open();
}
