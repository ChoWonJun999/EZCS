let lastChatbotMessage = "";

// DOM 콘텐츠가 완전히 로드되면 이 함수를 실행
document.addEventListener("DOMContentLoaded", function () {
    // 클래스가 "category-button"인 모든 요소를 선택
    const categoryButtons = document.querySelectorAll(".category-button");
    // 각 카테고리 버튼에 클릭 이벤트 리스너를 추가
    categoryButtons.forEach((button) => {
        button.addEventListener("click", function () {
            // 버튼이 클릭되면, 텍스트 내용을 가져와 selectCategory 호출
            const selectedCategory = this.textContent;
            selectCategory(selectedCategory);
        });
    });

    // 아이디가 "question"인 요소에 키다운 이벤트 리스너 추가
    document.getElementById("question").addEventListener("keydown", function (event) {
        // Shift 없이 Enter 키가 눌리면 기본 동작을 막고 sendMessage 호출
        if (event.keyCode === 13 && !event.shiftKey) {
            event.preventDefault();
            sendMessage(event);
        }
    });
});

// 선택된 카테고리를 저장하는 변수
let selectedCategory = null;

// 카테고리를 선택하는 함수
function selectCategory(category) {
    selectedCategory = category;
    console.log("Selected category:", selectedCategory);

    // 폼 데이터를 생성하고 카테고리와 CSRF 토큰 추가
    const formData = new FormData();
    formData.append("category", selectedCategory);
    formData.append("csrfmiddlewaretoken", getCookie("csrftoken"));

    // 서버로 POST 요청을 보내 카테고리를 설정
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
            document.getElementById("chat-content").innerHTML = ""; // 채팅 내용을 지움
            appendMessage("bot", data.initial_question); // 첫 질문 출력
            lastChatbotMessage = data.initial_question;
        })
        .catch((error) => console.error("Error:", error));
}

// 메시지를 전송하는 함수
function sendMessage(event) {
    event.preventDefault();
    const userInput = document.getElementById("question").value;
    if (!userInput.trim()) return;

    // 사용자 메시지를 채팅 상자에 추가
    appendMessage("user", userInput);

    // 사용자 메시지를 서버로 전송
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
            // 봇의 응답을 채팅 상자에 추가
            appendMessage("bot", data.response);
            lastChatbotMessage = data.response;
        })
        .catch((error) => console.error("Error:", error));
    textEvaluationToChatbot(userInput);
}

// 메시지를 채팅 상자에 추가하는 함수
function appendMessage(sender, message) {
    const messageElement = document.createElement("div");
    messageElement.className = "message-" + sender;
    messageElement.innerHTML = message;
    document.getElementById("chat-content").appendChild(messageElement);
    document.getElementById("question").value = "";
    document.getElementById("chat-content").scrollTop = document.getElementById("chat-content").scrollHeight;

    // 사용자의 메시지를 읽기 전용 채팅 상자에 추가
    if (sender === "user") {
        appendMessageToReadonly(sender, message);
    }
}

// 쿠키 값을 가져오는 함수
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// 시작 및 중지 버튼, 채팅 내용을 가져오는 변수
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
            interimDiv.className = 'interim-msg';
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
                    const formData = new FormData();
                    formData.append("message", finalTranscript);
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
                            // 봇의 응답을 채팅 상자에 추가
                            appendMessage("bot", data.response);
                            lastChatbotMessage = data.response;
                        })
                        .catch((error) => console.error("Error:", error));
                    textEvaluationToChatbot(finalTranscript);
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
    finalDiv.className = 'message-user';
    finalDiv.innerText = text;
    return finalDiv;
}

// 채팅 내용을 맨 아래로 스크롤
function scrollToBottom() {
    chatContent.scrollTop = chatContent.scrollHeight;
}

// 읽기 전용 채팅 상자에 메시지를 추가
function appendMessageToReadonly(sender, message) {
    const messageElement = document.createElement("div");
    messageElement.className = "message-" + sender;
    messageElement.innerHTML = message
    document.getElementById("readonly-chat-content").appendChild(messageElement);
    document.getElementById("readonly-chat-content").scrollTop = document.getElementById("readonly-chat-content").scrollHeight;
}

// 채팅 데이터를 저장하는 함수
function saveChatData() {
    const selectedCategory = document.getElementById('selected-category').innerText;
    const chatContent = document.getElementById('chat-content').innerText;

    const data = {
        category: selectedCategory,
        chat: chatContent,
        csrfmiddlewaretoken: '{{ csrf_token }}'
    };

    // 서버로 AJAX 요청을 보내 채팅 데이터를 저장
    $.ajax({
        type: 'POST',
        url: '{% url "save_chat_data" %}',  // URL을 동적으로 생성
        data: data,
        success: function (response) {
            alert('Data saved successfully');
        },
        error: function (response) {
            alert('Failed to save data');
        }
    });
}

// 텍스트 데이터를 챗봇에 전송하는 함수(view.py에 전송)
function textEvaluationToChatbot(userInput) {
    const formData = new FormData();

    console.log(lastChatbotMessage);

    formData.append('customerQuestion', lastChatbotMessage);
    formData.append('userInput', userInput);
    formData.append('category', selectedCategory);

    fetch('/education/evaluation_chat/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.output) {
                const childDiv = document.createElement('div');
                childDiv.className = 'evaluated-message-bot';
                childDiv.innerText = data.output;
                document.getElementById("readonly-chat-content").appendChild(childDiv);  // 챗봇 응답을 readonly-chat-content div에 추가
            } else if (data.error) {
                console.error('Error from server:', data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}