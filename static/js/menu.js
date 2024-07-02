// static/js/menu.js
document.addEventListener('DOMContentLoaded', function() {
              var dropdown = document.querySelector('.dropdown > a');
              var dropdownContent = document.querySelector('.dropdown-content');
          
              dropdown.addEventListener('click', function(event) {
                  event.preventDefault();
                  dropdownContent.classList.toggle('show');
              });
          });
          