document.addEventListener("DOMContentLoaded", function () {
    const categoryButtons = document.querySelectorAll(".category-button");
    categoryButtons.forEach((button) => {
        button.addEventListener("click", function () {
            const selectedCategory = this.textContent;
            selectCategory(selectedCategory);
        });
    });

    document.getElementById("question").addEventListener("keydown", function (event) {
        if (event.keyCode === 13 && !event.shiftKey) {
            event.preventDefault();
            sendMessage(event);
        }
    });
});

let selectedCategory = null;

function selectCategory(category) {
    selectedCategory = category;
    console.log("Selected category:", selectedCategory);

    const formData = new FormData();
    formData.append("category", selectedCategory);
    formData.append("csrfmiddlewaretoken", getCookie("csrftoken"));

    fetch("/education/", {
        method: "POST",
        body: formData
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then((data) => {
            console.log("Chatbot initialized:", data);
            document.getElementById("selected-category").innerText = selectedCategory;
            document.getElementById("chat-content").innerHTML = ""; // Clear chat content
            appendMessage("bot", data.initial_question); // 첫 질문 출력
        })
        .catch((error) => console.error("Error:", error));
}

function sendMessage(event) {
    event.preventDefault();
    const userInput = document.getElementById("question").value;
    if (!userInput.trim()) return;

    // Append user message to chat box
    appendMessage("user", userInput);

    // Send user message to server
    const formData = new FormData();
    formData.append("message", userInput);
    formData.append("csrfmiddlewaretoken", getCookie("csrftoken"));

    fetch("/education/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
        .then((response) => response.json())
        .then((data) => {
            // Append bot response to chat box
            appendMessage("bot", data.response);
        })
        .catch((error) => console.error("Error:", error));
}

function appendMessage(sender, message) {
    const messageElement = document.createElement("div");
    messageElement.className = "message " + sender;
    messageElement.innerHTML = message
        .split("\n")
        .map((line) => `<div>${line}</div>`)
        .join("");
    document.getElementById("chat-content").appendChild(messageElement);
    document.getElementById("question").value = "";
    document.getElementById("chat-content").scrollTop = document.getElementById("chat-content").scrollHeight;

    // Append user message to readonly chat box if sender is user
    if (sender === "user") {
        appendMessageToReadonly(sender, message);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const startButton = document.getElementById('start-button');
const stopButton = document.getElementById('stop-button');
const chatContent = document.getElementById('chat-content');
let mediaRecorder;
let audioChunks = [];

// 롤플레잉 시작 함수
function startEducation() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = 'ko-KR';
            let finalTranscript = '';

            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.start();

            // 기존의 interimDiv를 제거(중복생성 방지)
            removeExistingInterimDiv();

            // 새로운 interimDiv를 생성하여 추가
            const interimDiv = document.createElement('div');
            interimDiv.className = 'interim-msg message';
            chatContent.appendChild(interimDiv);

            // 음성 인식 시작 시 버튼 비활성화 및 로그 출력
            recognition.onstart = () => {
                startButton.disabled = true;
                stopButton.disabled = false;
                console.log('Education started');
            };

            // 음성 인식 결과 처리
            recognition.onresult = event => {
                let interimTranscript = '';
                const results = event.results;

                // 음성 인식을 실시간으로 보여주기 위한 for문
                for (let i = event.resultIndex; i < results.length; i++) {
                    if (results[i].isFinal) {
                        finalTranscript += results[i][0].transcript + ' ';
                    } else {
                        interimTranscript += results[i][0].transcript;
                    }
                }

                interimDiv.innerText = finalTranscript + interimTranscript;
                scrollToBottom();
            };

            // 음성 인식 오류 처리
            recognition.onerror = event => {
                console.error('Speech recognition error:', event.error);
                startButton.disabled = false;
                stopButton.disabled = true;
            };

            // 음성 인식 종료 시
            recognition.onend = () => {
                startButton.disabled = false;
                stopButton.disabled = true;
                console.log('Education ended');

                if (finalTranscript.trim() !== '') {
                    const finalDiv = createFinalDiv(finalTranscript);
                    chatContent.appendChild(finalDiv);
                    appendMessageToReadonly("user", finalTranscript);
                }

                interimDiv.remove();
                mediaRecorder.stop(); // 음성 녹음 중지
                scrollToBottom();
            };

            recognition.start();

            // 외부에서 종료할 수 있도록 recognition과 audioStream을 저장
            window.recognition = recognition;
            window.audioStream = stream;
        })
        .catch(error => {
            console.error('Error accessing media devices.', error);
        });
}

// 롤플레잉 종료 함수
function stopEducation() {
    if (window.recognition) {
        window.recognition.stop();
    }

    if (window.audioStream) {
        window.audioStream.getTracks().forEach(track => track.stop());
    }

    startButton.disabled = false;
    stopButton.disabled = true;

    // 녹음 중지 및 데이터 전송
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });

            if (userConfirmed) {
                // 사용자가 "네"를 선택한 경우 파일 저장 프로세스 진행
                sendAudioToServer(audioBlob);
            }
        };
    }
}

// interimDiv 제거 함수
function removeExistingInterimDiv() {
    const existingInterimDiv = document.querySelector('.interim-msg');
    if (existingInterimDiv) {
        existingInterimDiv.remove();
    }
}

// output-msg 생성(종료 버튼 클릭시 동작)
function createFinalDiv(text) {
    const finalDiv = document.createElement('div');
    finalDiv.className = 'message user';
    finalDiv.innerText = text;
    return finalDiv;
}

function scrollToBottom() {
    chatContent.scrollTop = chatContent.scrollHeight;
}

function appendMessageToReadonly(sender, message) {
    const messageElement = document.createElement("div");
    messageElement.className = "message " + sender;
    messageElement.innerHTML = message
        .split("\n")
        .map((line) => `<div>${line}</div>`)
        .join("");
    document.getElementById("readonly-chat-content").appendChild(messageElement);
    document.getElementById("readonly-chat-content").scrollTop = document.getElementById("readonly-chat-content").scrollHeight;
}

function saveChatData() {
    const selectedCategory = document.getElementById('selected-category').innerText;
    const chatContent = document.getElementById('chat-content').innerText;

    const data = {
        category: selectedCategory,
        chat: chatContent,
        csrfmiddlewaretoken: '{{ csrf_token }}'
    };

    $.ajax({
        type: 'POST',
        url: '{% url "save_chat_data" %}',  // URL을 동적으로 생성
        data: data,
        success: function(response) {
            alert('Data saved successfully');
        },
        error: function(response) {
            alert('Failed to save data');
        }
    });
}