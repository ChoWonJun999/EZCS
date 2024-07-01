function check_login(event) {
    let param = {
        username: $("#loginUsername").val(),
        password: $("#loginPassword").val(),
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

function check_admin_login(event) {
    let param = {
        username: $("#loginUsername").val(),
        password: $("#loginPassword").val(),
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
            if (data.result != "success") {
                alert(data.result);
            } else {
                location.href = "/management/";
            }
        }
    });
}

$(document).ready(function () {
    $("#loginForm").on("submit", check_admin_login);
});

function showSignupForm() {
    document.getElementById("loginForm").style.display = "none";
    document.getElementById("signupForm").style.display = "block";
    document.getElementById("forgotPasswordForm").style.display = "none";
    document.getElementById("adminLoginForm").style.display = "none";
    document.getElementById("authTitle").innerText = "회원가입";
}

function showForgotPasswordForm() {
    document.getElementById("loginForm").style.display = "none";
    document.getElementById("signupForm").style.display = "none";
    document.getElementById("forgotPasswordForm").style.display = "block";
    document.getElementById("adminLoginForm").style.display = "none";
    document.getElementById("authTitle").innerText = "비밀번호 찾기";
}

function showLoginForm() {
    document.getElementById("loginForm").style.display = "block";
    document.getElementById("signupForm").style.display = "none";
    document.getElementById("forgotPasswordForm").style.display = "none";
    document.getElementById("adminLoginForm").style.display = "none";
    document.getElementById("authTitle").innerText = "로그인";
}

function login() {
    var username = document.getElementById("loginUsername").value;
    var password = document.getElementById("loginPassword").value;

    console.log("ID:", username);
    console.log("PW:", password);

    // 실제 인증 로직을 추가해야 함.
    // 예: 서버로 사용자명과 암호를 전송하여 인증 처리
}

function showAdminLoginForm() {
    document.getElementById("loginForm").style.display = "none";
    document.getElementById("signupForm").style.display = "none";
    document.getElementById("forgotPasswordForm").style.display = "none";
    document.getElementById("adminLoginForm").style.display = "block";
    document.getElementById("authTitle").innerText = "관리자 로그인";
}

function adminLogin() {
    var adminUsername = document.getElementById("adminUsername").value;
    var adminPassword = document.getElementById("adminPassword").value;

    console.log("관리자 ID:", adminUsername);
    // console.log('관리자 PW:', adminPassword); // 비밀번호 출력 제거

    // 실제 관리자 인증 로직을 서버 측에서 처리해야 함.
    // 예: 서버로 관리자 계정으로 인증 요청을 보내고, 결과에 따라 사용자 경험을 관리
    // 여기서는 클라이언트 측에서는 로그인 폼만 표시하도록 설정
}

function hideAdminLoginForm() {
    document.getElementById("adminLoginForm").reset();
    document.getElementById("loginForm").style.display = "block";
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
    console.log("비밀번호:", password); // 비밀번호 출력 제거
    console.log("생년월일:", birthdate);
    console.log("이메일:", email);
    console.log("주소:", address);
    console.log("우편번호:", postcode);

    // 실제 회원가입 로직을 추가해야 함.
    // 예: 서버로 이메일, 이름, 주소, 비밀번호, 생년월일, 우편번호를 전송하여 회원가입 처리
}

function sendPasswordResetEmail() {
    var username = document.getElementById("forgotPasswordUsername").value;

    console.log("비밀번호 재설정 요청 이메일:", username);

    // 실제 비밀번호 재설정 이메일 발송 로직을 추가해야 함.
    // 예: 서버로 사용자 이메일을 전송하여 비밀번호 재설정 이메일을 발송하는 처리
}

function searchPostcode() {
    // 우편번호 검색 기능 구현
    var postcode = document.getElementById("postcode").value;

    console.log("우편번호 검색:", postcode);

    // 여기에 우편번호 서비스 API를 호출?? <자체 데이터베이스에서 검색하여 주소 정보를 가져오는 처리>
}
