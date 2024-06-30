function check_login(event) {
    event.preventDefault(); // 폼 제출 방지

    let param = {
        username: $("#loginUsername").val(),
        password: $("#loginPassword").val()
    };

    $.ajax({
        url: "{% url 'accounts:login' %}",
        type: "post",
        data: param,
        dataType: "json",
        headers: {
            "X-CSRFToken": "{{ csrf_token }}"
        },
        success: function (data) {
            if (data.result != "success") {
                alert(data.result);
            } else {
                location.href = "/";
            }
        }
    });
}

$(document).ready(function () {
    $("#loginForm").on("submit", check_login);
});

function showSignupForm() {
    document.getElementById("loginForm").style.display = "none";
    document.getElementById("signupForm").style.display = "block";
    document.getElementById("forgotPasswordForm").style.display = "none";
    document.getElementById("authTitle").innerText = "회원가입";
}

function showForgotPasswordForm() {
    document.getElementById("loginForm").style.display = "none";
    document.getElementById("signupForm").style.display = "none";
    document.getElementById("forgotPasswordForm").style.display = "block";
    document.getElementById("authTitle").innerText = "비밀번호 찾기";
}

function showLoginForm() {
    document.getElementById("loginForm").style.display = "block";
    document.getElementById("signupForm").style.display = "none";
    document.getElementById("forgotPasswordForm").style.display = "none";
    document.getElementById("authTitle").innerText = "로그인";
}

function signup() {
    var name = document.getElementById("name").value;
    var address = document.getElementById("address").value;
    var password = document.getElementById("password").value;
    var email = document.getElementById("email").value;
    var birthdate = document.getElementById("birthdate").value;
    var postcode = document.getElementById("postcode").value;

    console.log("이름:", name);
    console.log("비밀번호:", password);
    console.log("생년월일:", birthdate);
    console.log("이메일:", email);
    console.log("주소:", address);
    console.log("우편번호:", postcode);

    // 실제 회원가입 로직을 추가해야 합니다.
    // 예: 서버로 이메일, 이름, 주소, 비밀번호, 생년월일, 우편번호를 전송하여 회원가입 처리
}

function sendPasswordResetEmail() {
    var username = document.getElementById("forgotPasswordUsername").value;

    console.log("비밀번호 재설정 요청 이메일:", username);

    // 실제 비밀번호 재설정 이메일 발송 로직을 추가해야 합니다.
    // 예: 서버로 사용자 이메일을 전송하여 비밀번호 재설정 이메일을 발송하는 처리
}

function searchPostcode() {
    // 우편번호 검색 기능 구현
    var postcode = document.getElementById("postcode").value;

    console.log("우편번호 검색:", postcode);

    // 여기에 우편번호 서비스 API를 호출하여 주소 정보를 가져오는 처리
}
