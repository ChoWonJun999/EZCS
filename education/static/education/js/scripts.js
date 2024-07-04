document.addEventListener('DOMContentLoaded', function () {
    const categoryButtons = document.querySelectorAll('.category-button');
    categoryButtons.forEach(button => {
        button.addEventListener('click', function () {
            const selectedCategory = this.textContent;
            selectCategory(selectedCategory);
        });
    });

    document.getElementById("question").addEventListener("keydown", function(event) {
        if (event.keyCode === 13 && !event.shiftKey) {
            event.preventDefault();
            document.getElementById("text-button").click();
        }
    });
});

let selectedCategory = null;

function selectCategory(category) {
    selectedCategory = category;
    console.log('Selected category:', selectedCategory);

    const formData = new FormData();
    formData.append('category', selectedCategory);
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

    fetch('/education/', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Chatbot initialized:', data);
        document.getElementById('selected-category').innerText = selectedCategory;
        appendMessage('bot', data.initial_question); // 첫 질문 출력
    })
    .catch(error => console.error('Error:', error));
}

function sendMessage(event) {
    event.preventDefault();
    const userInput = document.getElementById('question').value;
    if (!userInput.trim()) return;

    // Append user message to chat box
    appendMessage('user', userInput);

    // Send user message to server
    const formData = new FormData();
    formData.append('message', userInput);
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

    fetch('/education/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        // Append bot response to chat box
        appendMessage('bot', data.response);
    })
    .catch(error => console.error('Error:', error));
}

function appendMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.className = 'message ' + sender;
    messageElement.innerHTML = message.split('\n').map(line => `<div>${line}</div>`).join('');
    document.getElementById('chat-content').appendChild(messageElement);
    document.getElementById('question').value = '';
    document.getElementById('chat-content').scrollTop = document.getElementById('chat-content').scrollHeight;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
