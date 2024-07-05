$(document).ready(function () {
    $("tr[data-url]").click(function () {
        var url = $(this).data("url");
        window.location.href = url;
    });
});