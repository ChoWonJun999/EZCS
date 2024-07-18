function validatePassword(password) {
    // 최소 8자 이상, 하나 이상의 소문자, 숫자, 특수문자를 포함해야 함
    var passwordRegex = /^(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[a-z\d@$!%*?&]{8,}$/;
    return passwordRegex.test(password);
}

function submitProfile() {
    let name = $("#name").val();
    let emailLocal = $("#emailLocal").val();
    let emailDomain = $("#emailDomain").val();
    let email = emailLocal + "@" + emailDomain;
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
        alert("비밀번호는 최소 8자 이상이어야 하며, 소문자, 숫자, 특수문자를 포함해야 합니다.");
        return false;
    }

    if (!confirm("변경된 사항을 저장하시겠습니까?")) {
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
                document.getElementById("address").value = "";
            }

            // 선택된 우편번호와 주소 정보를 input 박스에 넣는다.
            document.getElementById("address_code").value = data.zonecode;
            document.getElementById("address").value = addr;
            document.getElementById("address").value += extraAddr;
            document.getElementById("address_detail").focus(); // 우편번호 + 주소 입력이 완료되었음으로 상세주소로 포커스 이동
        }
    }).open();
}

function emailDomainChange(obj) {
    $("#emailDomain").val(obj.value);
    if (obj.value == "") {
        $("#emailDomain").attr("disabled", false);
    } else {
        $("#emailDomain").attr("disabled", true);
    }
}

$(document).ready(function () {
    $("#birth_date").val(new Date($("#birth_date").val()).toISOString().slice(0, 10));

    $("#editProfileForm").on("submit", function(event) {
        event.preventDefault();
        submitProfile();
    });
});
