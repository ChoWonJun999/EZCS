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