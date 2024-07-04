document.addEventListener("DOMContentLoaded", function () {
    var accordions = document.querySelectorAll(".accordion-toggle");
    accordions.forEach(function (accordion) {
        accordion.addEventListener("click", function () {
            var content = this.nextElementSibling;
            var allContents = document.querySelectorAll(".accordion-content");
            allContents.forEach(function (otherContent) {
                if (otherContent !== content) {
                    otherContent.classList.remove("show");
                }
            });
            content.classList.toggle("show");
        });
    });
});


// test

document.querySelectorAll('.has-submenu > a').forEach(menu => {
    menu.addEventListener('click', (e) => {
        e.preventDefault();
        const parent = menu.parentElement;
        parent.classList.toggle('open');
        parent.querySelector('.submenu').style.display = parent.classList.contains('open') ? 'block' : 'none';
    });
});

const darkModeToggle = document.getElementById('darkModeToggle');
darkModeToggle.addEventListener('change', (event) => {
    if (event.target.checked) {
        document.body.style.backgroundColor = '#333';
        document.body.style.color = '#fff';
    } else {
        document.body.style.backgroundColor = '#f5f7fb';
        document.body.style.color = '#000';
    }
});
