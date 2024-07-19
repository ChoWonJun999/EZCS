let lastChatbotMessage = "";
const loadingDiv = document.querySelector(".loading");

// DOM 콘텐츠가 완전히 로드되면 이 함수를 실행
document.addEventListener("DOMContentLoaded", function () {
    // 아이디가 "question"인 요소에 키다운 이벤트 리스너 추가
    document.getElementById("question").addEventListener("keydown", function (event) {
        // Shift 없이 Enter 키가 눌리면 기본 동작을 막고 sendMessage 호출
        if (event.keyCode === 13 && !event.shiftKey) {
            event.preventDefault();
            sendMessage(event);
        }
    });
});

// 카테고리를 선택하는 함수
function selectCategory(category) {
    console.log("Selected category:", category);

    loadingDiv.style.display = "flex";

    // 선택한 순간 버튼 비활성화
    ableCategoryButtons(true);

    // 폼 데이터를 생성하고 카테고리와 CSRF 토큰 추가
    const formData = new FormData();
    formData.append("category", category);

    // 서버로 POST 요청을 보내 카테고리를 설정
    fetch("/education/", {
        method: "POST",
        headers: {
            "X-CSRFToken": $("#csrf").val()
        },
        body: formData
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            loadingDiv.style.display = "none";
            return response.json();
        })
        .then((data) => {
            console.log("Chatbot initialized:", data);
            $("#category-selected").val(category);
            $("#log-header").val(data.log_header);

            document.getElementById("selected-category").innerText = category;
            document.getElementById("chat-content").innerHTML = ""; // 채팅 내용을 지움
            appendMessage("bot", data.initial_question); // 첫 질문 출력
            textToSpeech(data.initial_question);

            windowChange(true);
        })
        .catch((error) => {
            console.error("Error:", error);
            ableCategoryButtons(false);
            alert("ERROR");
        });
}

// 메시지를 전송하는 함수
function sendMessage(event) {
    event.preventDefault();
    const message = document.getElementById("question").value;
    if (!message.trim()) return;

    // 사용자 메시지를 채팅 상자에 추가
    appendMessage("user", message);

    appendMessage("interim", "AI가 메시지를 생성중입니다  <div class='spinner-grow spinner-grow-sm' role='status'></div>");

    // 사용자 메시지를 서버로 전송
    const formData = new FormData();
    formData.append("message", message);
    formData.append("category", $("#category-selected").val());
    formData.append("log_header", $("#log-header").val());

    fetch("/education/", {
        method: "POST",
        headers: {
            "X-CSRFToken": $("#csrf").val()
        },
        body: formData
    })
        .then((response) => response.json())
        .then((data) => {
            // 봇의 응답을 채팅 상자에 추가
            appendMessage("bot", data.response);
            // lastChatbotMessage = data.response;
            removeMessageInterimDiv();
            textToSpeech(data.response);

            if (data.output) {
                const childDiv = document.createElement("div");
                childDiv.className = "evaluated-message-bot";
                childDiv.innerText = data.output;
                document.getElementById("readonly-chat-content").appendChild(childDiv);
            } else if (data.error) {
                console.error("Error from server:", data.error);
            }
        })
        .catch((error) => {
            removeMessageInterimDiv();
            console.error("Error:", error);
        });
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

// 시작 및 중지 버튼, 채팅 내용을 가져오는 변수
const startButton = document.getElementById("start-button");
const stopButton = document.getElementById("stop-button");
const chatContent = document.getElementById("chat-content");
let mediaRecorder;
let audioChunks = [];

// 롤플레잉 시작 함수
function startEducation() {
    $("#question").attr("readonly", true);
    $("#text-button").attr("disabled", true);

    navigator.mediaDevices
        .getUserMedia({ audio: true })
        .then((stream) => {
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = "ko-KR";
            let finalTranscript = "";

            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };

            mediaRecorder.start();

            // 기존의 interimDiv를 제거(중복생성 방지)
            removeExistingInterimDiv();

            // 새로운 interimDiv를 생성하여 추가
            const interimDiv = document.createElement("div");
            interimDiv.className = "interim-msg";
            chatContent.appendChild(interimDiv);

            // 음성 인식 시작 시 버튼 비활성화 및 로그 출력
            recognition.onstart = () => {
                startButton.disabled = true;
                stopButton.disabled = false;
                console.log("Education started");
            };

            // 음성 인식 결과 처리
            recognition.onresult = (event) => {
                let interimTranscript = "";
                const results = event.results;

                // 음성 인식을 실시간으로 보여주기 위한 for문
                for (let i = event.resultIndex; i < results.length; i++) {
                    if (results[i].isFinal) {
                        finalTranscript += results[i][0].transcript + " ";
                    } else {
                        interimTranscript += results[i][0].transcript;
                    }
                }

                interimDiv.innerText = finalTranscript + interimTranscript;
                scrollToBottom();
            };

            // 음성 인식 오류 처리
            recognition.onerror = (event) => {
                console.error("Speech recognition error:", event.error);
                startButton.disabled = false;
                stopButton.disabled = true;
            };

            // 음성 인식 종료 시
            recognition.onend = () => {
                startButton.disabled = false;
                stopButton.disabled = true;
                console.log("Education ended");

                if (finalTranscript.trim() !== "") {
                    const finalDiv = createFinalDiv(finalTranscript);
                    chatContent.appendChild(finalDiv);
                    appendMessage("interim", "AI가 메시지를 생성중입니다  <div class='spinner-grow spinner-grow-sm' role='status'></div>");
                    appendMessageToReadonly("user", finalTranscript);

                    const formData = new FormData();
                    formData.append("message", finalTranscript);
                    formData.append("category", $("#category-selected").val());
                    formData.append("log_header", $("#log-header").val());

                    fetch("/education/", {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": $("#csrf").val()
                        },
                        body: formData
                    })
                        .then((response) => response.json())
                        .then((data) => {
                            // 봇의 응답을 채팅 상자에 추가
                            removeMessageInterimDiv();
                            appendMessage("bot", data.response);
                            if (data.output) {
                                const childDiv = document.createElement("div");
                                childDiv.className = "evaluated-message-bot";
                                childDiv.innerText = data.output;
                                document.getElementById("readonly-chat-content").appendChild(childDiv);
                            } else if (data.error) {
                                console.error("Error from server:", data.error);
                            }
                        })
                        .catch((error) => {
                            console.error("Error:", error);
                            removeMessageInterimDiv();
                        });
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
        .catch((error) => {
            console.error("Error accessing media devices.", error);
        });
}

// 롤플레잉 종료 함수
function stopEducation() {
    $("#question").attr("readonly", false);
    $("#text-button").attr("disabled", false);
    if (window.recognition) {
        window.recognition.stop();
    }

    if (window.audioStream) {
        window.audioStream.getTracks().forEach((track) => track.stop());
    }

    startButton.disabled = false;
    stopButton.disabled = true;

    // 녹음 중지 및 데이터 전송
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: "audio/webm" });

            if (userConfirmed) {
                // 사용자가 "네"를 선택한 경우 파일 저장 프로세스 진행
                sendAudioToServer(audioBlob);
            }
        };
    }
}

function ableCategoryButtons(bool) {
    const buttons = document.querySelectorAll(".category-button");
    buttons.forEach((button) => {
        button.disabled = bool;
        if (bool) {
            button.style.cursor = "not-allowed";
        } else {
            button.style.cursor = "pointer";
        }
    });
}

// interimDiv 제거 함수
function removeExistingInterimDiv() {
    const existingInterimDiv = document.querySelector(".interim-msg");
    if (existingInterimDiv) {
        existingInterimDiv.remove();
    }
}

function removeMessageInterimDiv() {
    const existingInterimDiv = document.querySelector(".message-interim");
    if (existingInterimDiv) {
        existingInterimDiv.remove();
    }
}

// output-msg 생성(종료 버튼 클릭시 동작)
function createFinalDiv(text) {
    const finalDiv = document.createElement("div");
    finalDiv.className = "message-user";
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
    messageElement.innerHTML = message;
    document.getElementById("readonly-chat-content").appendChild(messageElement);
    document.getElementById("readonly-chat-content").scrollTop = document.getElementById("readonly-chat-content").scrollHeight;
}

function resetToCategorySelection(obj) {
    location.href = $(obj).data("url");
}

function windowChange(bool) {
    document.getElementById("category-selection").classList.toggle("hidden", bool);
    document.getElementById("guide-section").classList.toggle("hidden", bool);
    document.getElementById("chat-section").classList.toggle("hidden", !bool);
    document.getElementById("chat-section-readonly").classList.toggle("hidden", !bool);
    document.getElementById("submit-container").classList.toggle("hidden", !bool);
}

function textToSpeech(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "ko-KR"; // 한국어 설정
    utterance.rate = 2;
    speechSynthesis.speak(utterance);

    window.addEventListener('beforeunload', () => {
        speechSynthesis.cancel();
    });
}
