$(document).ready(function () {
    $("tr[data-url]").click(function () {
        var url = $(this).data("url");
        window.location.href = url;
    });
});

function approval(obj) {
    if (confirm($(obj).data("username") + "님의 요청 승인하시겠습니까??") == true) {
        let url = $(obj).data("url");
        location.href = url;
    } else {
        return false;
    }
}
