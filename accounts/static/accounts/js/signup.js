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

    let password = $("#password").val();
    let password_confirm = $("#pwChk").val();

    if (password != password_confirm) {
        alert("비번 다름");
        return false;
    }
    // email: $("#email").val() + "@" + $("#emailadd").val(),
    $("#addressCode").removeAttr("disabled");
    let param = {
        username: username,
        password: password,
        name: name,

        email: "temp@temp.com",
        birthdate: $("#birthdate").val(),
        addressCode: $("#addressCode").val(),
        address: $("#UserAdd1").val(),
        addressDetail: $("#UserAdd2").val()
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
            $("#addressCode").attr("disabled");
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

            document.getElementById("addressCode").value = data.zonecode;
            document.getElementById("UserAdd1").value = addr;
            document.getElementById("UserAdd1").value += extraAddr;
            document.getElementById("UserAdd2").focus();
        }
    }).open();
}
