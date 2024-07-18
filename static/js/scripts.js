document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");
    const sidebarToggle = document.getElementById("sidebarToggle");

    sidebarToggle.addEventListener("click", function () {
        sidebar.classList.toggle("hidden");
        sidebarToggle.classList.toggle("active");
    });

    function handleResize() {
        if (window.innerWidth > 768) {
            sidebar.classList.remove("hidden");
            sidebarToggle.classList.remove("active");
            sidebarToggle.style.display = "none";
        } else {
            sidebar.classList.add("hidden");
            sidebarToggle.style.display = "block";
        }
    }

    window.addEventListener("resize", handleResize);
    handleResize(); // 초기 로드 시 사이드바 상태 설정
});


$(document).ready(function() {
    // 내 정보 클릭 시 모달 표시
    $("#profileLink").on("click", function() {
        $("#passwordModal").modal("show");
    });

    // 모달이 완전히 표시된 후에 포커스 설정
    $("#passwordModal").on('shown.bs.modal', function () {
        $("#passwordCheck").focus();
    });

    // 엔터 키 이벤트 처리
    $("#passwordCheck").on("keypress", function(e) {
        if (e.which == 13) {
            checkPassword();
        }
    });

    // 확인 버튼 클릭 시 비밀번호 검증
    $("#passwordCheckButton").on("click", function() {
        checkPassword();
    });
});

function checkPassword() {
    var password = $("#passwordCheck").val();
    var csrfToken = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
        url: "/verify-password/",
        type: "POST",
        data: {
            password: password,
            csrfmiddlewaretoken: csrfToken
        },
        success: function(response) {
            if (response.valid) {
                window.location.href = "/edit_profile/";
            } else {
                $("#passwordCheckError").show();
            }
        }
    });
}

