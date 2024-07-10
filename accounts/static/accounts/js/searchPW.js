function ResetPW() {
    var width = 800;
    var height = 600;
    var left = (screen.width - width) / 2;
    var top = (screen.height - height) / 2;
    var resetPWurl = "{% url 'accounts:reset_password' %}";

    let username = $("#forgotPasswordUsername").val();
    let birthdate = $("#birthdate").val();
    let phone_number = $("#phone_number").val();

    if (!username || !birthdate || !phone_number) {
        alert("모든 필드를 채워주세요.");
        return;
    }

    let data = {
        username: username,
        birthdate: birthdate,
        phone_number: phone_number
    };

    let form = $("#searchPWForm");
    let url = form.data("url");
    let csrf = $("input[name=csrf]").val();

    $.ajax({
        url: url,
        type: "post",
        data: data,
        dataType: "json",
        headers: {
            "X-CSRFToken": csrf
        },
        success: function (response) {
            if (response.result === 'success') {
                alert(response.msg);
                window.open("{% url 'accounts:reset_password' %}", "Reset PassWord", "width=" + width + ",height=" + height + ",top=" + top + ",left=" + left);
            } else {
                alert(response.msg);
            }
        },
        error: function (xhr, status, error) {
            alert("요청 중 오류가 발생했습니다. 다시 시도해 주세요.");
        }
    });
}