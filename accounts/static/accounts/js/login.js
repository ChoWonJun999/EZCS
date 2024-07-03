function check_login(obj) {
    username = $("#loginUsername");
    password = $("#loginPassword");
    rememberMe = $("#rememberMe").is(":checked") ? "on" : "off";

    if (username.val() == "") {
        alert("아이디 입력");
        username.focus();
        return;
    }
    if (password.val() == "") {
        alert("password 입력");
        password.focus();
        return;
    }

    let param = {
        username: username.val(),
        password: password.val(),
        remember_me: rememberMe
    };

    var from = $("#loginForm");
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
            if (data.result != "user" && data.result != "manager") {
                alert(data.result);
            } else {
                if ((obj == 0 && data.result == "user") || (obj == 0 && data.result == "manager")) {
                    location.href = "/";
                } else if (obj == 1 && data.result == "manager") {
                    location.href = "/management";
                } else {
                    alert("관리자 권한이 없습니다.");
                }
            }
        }
    });
}

$(document).ready(function () {
    $("#loginUsername").focus();
    $("#loginPassword").keypress(function (event) {
        if (event.which == 13) {
            check_login(0);
        }
    });
});

function execDaumPostcode() {
    new daum.Postcode({
        oncomplete: function (data) {
            // 팝업을 통한 검색 결과 항목 클릭 시 실행
            var addr = ""; // 주소_결과값이 없을 경우 공백
            var extraAddr = ""; // 참고항목

            //사용자가 선택한 주소 타입에 따라 해당 주소 값을 가져온다.
            if (data.userSelectedType === "R") {
                // 도로명 주소를 선택
                addr = data.roadAddress;
            } else {
                // 지번 주소를 선택
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
            } else {
                document.getElementById("UserAdd1").value = "";
            }

            // 선택된 우편번호와 주소 정보를 input 박스에 넣는다.
            document.getElementById("zipp_code_id").value = data.zonecode;
            document.getElementById("UserAdd1").value = addr;
            document.getElementById("UserAdd1").value += extraAddr;
            document.getElementById("UserAdd2").focus(); // 우편번호 + 주소 입력이 완료되었음으로 상세주소로 포커스 이동
        }
    }).open();
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
