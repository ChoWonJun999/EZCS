const transcription = document.getElementById("transcription");
const translationContent = document.getElementById("translation-content");
let mediaRecorder;
let audioChunks = [];
let recognition;
let currentStream;
let audioBlob;
let currentInterimDiv;

function updateLog() {
    let phone_number = $("#phone").val();
    if (phone_number.length !== 11 || !/^\d{11}$/.test(phone_number)) {
        alert("전화번호는 11자리 숫자여야 합니다.");
        return;
    }

    const form = document.getElementById("customer-form");

    const formData = new FormData(form);
    formData.append("logId", $("#logId").val());
    formData.append("inquiries", $("#inquiry-text").val());
    formData.append("action", $("#action-text").val());
    fetch(form.action, {
        method: "POST",
        headers: { "X-CSRFToken": $("#csrf").val() },
        body: formData
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert("문의/조치내용이 저장되었습니다.");
            } else {
                alert("문의/조치내용 저장에 실패했습니다.");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}

function saveCustomerInfo() {
    // 고객 정보 수정 저장 버튼
    let phone_number = $("#phone").val();

    const form = document.getElementById("customer-form");
    const inputs = form.querySelectorAll('input:not([type="button"])');

    // 고객 정보를 저장하는 로직 추가, 예: 서버로 데이터 전송
    if (phone_number.length !== 11 || !/^\d{11}$/.test(phone_number)) {
        alert("전화번호는 11자리 숫자여야 합니다.");
        return;
    }

    const formData = new FormData(form);
    fetch(form.action, {
        method: "POST",
        headers: { "X-CSRFToken": $("#csrf").val() },
        body: formData
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert("고객 정보가 저장되었습니다.");
            } else {
                alert("고객 정보 저장에 실패했습니다.");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("고객 정보 저장 중 오류가 발생했습니다.");
        });

    inputs.forEach((input) => (input.disabled = true));
    form.querySelector(".edit-button").style.display = "inline-block";
    form.querySelectorAll(".save-button, .cancel-button").forEach((button) => {
        button.style.display = "none";
    });
}

function cancelEdit() {
    // 고객 정보 수정 취소 버튼
    const form = document.getElementById("customer-form");
    const inputs = form.querySelectorAll('input:not([type="button"])');
    inputs.forEach((input) => (input.disabled = true));

    // 수정 취소를 처리하는 로직 추가, 예: 변경 사항 되돌리기
    // alert('수정이 취소되었습니다.');

    form.querySelector(".edit-button").style.display = "inline-block";
    form.querySelectorAll(".save-button, .cancel-button").forEach((button) => {
        button.style.display = "none";
    });
}

// 기본 메시지 저장
const defaultTranscriptionMessage = transcription.innerHTML;

function startCounseling(type) {
    navigator.mediaDevices
        .getUserMedia({ audio: true })
        .then((stream) => {
            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = "ko-KR";
            let finalTranscript = "";

            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            currentStream = stream;

            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };

            mediaRecorder.start();

            recognition.onstart = () => {
                changeDisabled(true);

                console.log("Counseling started");

                // 기존 interimDiv 제거
                removeExistingInterimDiv();

                // 새로운 interimDiv 생성
                currentInterimDiv = document.createElement("div");
                currentInterimDiv.className = "interim-msg";
                transcription.appendChild(currentInterimDiv);
                scrollToBottom(); // 항상 하단으로 스크롤
            };

            recognition.onresult = (event) => {
                let interimTranscript = "";
                const results = event.results;

                for (let i = event.resultIndex; i < results.length; i++) {
                    if (results[i].isFinal) {
                        finalTranscript += results[i][0].transcript + " ";
                    } else {
                        interimTranscript += results[i][0].transcript;
                    }
                }

                // interim 메시지 업데이트
                currentInterimDiv.innerHTML = (type === "customer" ? "<strong>고객:</strong> " : "<strong>상담원:</strong> ") + finalTranscript + interimTranscript;
                scrollToBottom(); // 항상 하단으로 스크롤
            };

            recognition.onerror = (event) => {
                console.error("Speech recognition error:", event.error);
                changeDisabled(false);
            };

            recognition.onend = () => {
                changeDisabled(false);

                console.log("Counseling ended");

                if (finalTranscript.trim() !== "") {
                    const finalDiv = createFinalDiv(finalTranscript, type);
                    transcription.appendChild(finalDiv);
                    loadAIMessages(type, finalTranscript);
                }

                mediaRecorder.stop();

                // interim 메시지 제거
                removeExistingInterimDiv();

                // 기본 메시지를 다시 표시하지 않음
                if (transcription.innerHTML.trim() === "") {
                    transcription.innerHTML = defaultTranscriptionMessage;
                }
                scrollToBottom(); // 항상 하단으로 스크롤
            };

            recognition.start();

            window.recognition = recognition;
            window.audioStream = stream;
        })
        .catch((error) => {
            console.error("Error accessing media devices.", error);
        });
}

function stopCounseling() {
    if (recognition) {
        recognition.stop();
    }

    if (currentStream) {
        currentStream.getTracks().forEach((track) => track.stop());
    }

    changeDisabled(false);

    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
        mediaRecorder.onstop = () => {
            audioBlob = new Blob(audioChunks, { type: "audio/webm" });
        };
    }
}

function loadAIMessages(classify, message) {
    if (data.success && classify === "customer") appendAILoading();

    const formData = new FormData();
    formData.append("classify", classify);
    formData.append("message", message);
    formData.append("logId", $("#logId").val());

    fetch($("#url").val(), {
        method: "POST",
        headers: { "X-CSRFToken": $("#csrf").val() },
        body: formData
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success && classify === "customer") {
                removeAILoading();
                addCustomerMessageToTranslationContent(data.trans_output);
                const childDiv = document.createElement("div");
                childDiv.className = "chatbot-response";
                childDiv.innerText = data.recommend_output;
                translationContent.appendChild(childDiv);
            }
        })
        .catch((error) => {
            removeAILoading();
            console.error("Error:", error);
            alert("ERROR:", error);
        });
}

function changeDisabled(bool) {
    document.getElementById("customer-start-button").disabled = bool;
    document.getElementById("counselor-start-button").disabled = bool;
    document.getElementById("stop-button").disabled = !bool;
    document.getElementById("save-button").disabled = bool;
}

function removeExistingInterimDiv() {
    const existingInterimDiv = document.querySelector(".interim-msg");
    if (existingInterimDiv) {
        existingInterimDiv.remove();
    }
}

function createFinalDiv(text, type) {
    const finalDiv = document.createElement("div");
    finalDiv.className = `output-msg ${type}`;
    finalDiv.innerHTML = (type === "customer" ? "<strong>고객:</strong> " : "<strong>상담원:</strong> ") + text;
    return finalDiv;
}

function addCustomerMessageToTranslationContent(text) {
    const translationDiv = document.createElement("div");
    translationDiv.className = "output-msg customer";
    translationDiv.innerHTML = "<strong>번역:</strong> " + text;
    translationContent.appendChild(translationDiv);
}

function saveCounselingLog() {
    const raw_data = [];
    const chatbot_data = [];

    let phone_number = $("#phone").val();

    // 전화번호 유효성 검사
    if (phone_number.length !== 11 || !/^\d{11}$/.test(phone_number)) {
        alert("고객의 전화번호를 입력하여주세요.");
        return;
    }

    const inquiry_text = document.getElementById("inquiry-text").value;
    const action_text = document.getElementById("action-text").value;

    // 채팅 내역에서 필요한 요소를 가져옴
    const transcriptionElements = document.querySelectorAll("#transcription .output-msg, #transcription .chatbot-response");
    const translationElements = document.querySelectorAll("#translation-content .output-msg, #translation-content .chatbot-response");

    // 요소들의 순서대로 인덱스 번호를 매김
    transcriptionElements.forEach((element, index) => {
        if (element.classList.contains("customer")) {
            raw_data.push({
                index: index + 1,
                type: "customer",
                text: element.innerText.replace("고객:", "").trim()
            });
        } else if (element.classList.contains("counselor")) {
            raw_data.push({
                index: index + 1,
                type: "counselor",
                text: element.innerText.replace("상담원:", "").trim()
            });
        }
    });

    // 챗봇 데이터는 별개로 인덱스를 매김
    translationElements.forEach((element, index) => {
        if (element.classList.contains("customer")) {
            chatbot_data.push({
                index: index + 1,
                type: "translated",
                text: element.innerText.replace("번역:", "").trim()
            });
        } else if (element.classList.contains("chatbot-response")) {
            chatbot_data.push({
                index: index + 1,
                type: "chatbot",
                text: element.innerText.trim()
            });
        }
    });

    console.log(window.username);
    // 상담 로그 데이터 객체 생성
    const counselingLog = {
        username: window.username,
        phone_number: phone_number,
        chat_data: {
            raw_data: raw_data,
            chatbot_data: chatbot_data
        },
        memo_data: {
            inquiry_text: inquiry_text,
            action_text: action_text
        }
    };

    // 상담 로그 데이터 서버로 전송
    fetch("/counseling/save_counseling_log/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": $("#csrf").val()
        },
        body: JSON.stringify(counselingLog)
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert("상담 로그가 저장되었습니다.");
            } else {
                alert("상담 로그 저장에 실패했습니다.");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("상담 로그 저장 중 오류가 발생했습니다.");
        });
    
}

function scrollToBottom() {
    transcription.scrollTop = transcription.scrollHeight;
}

function appendAILoading() {
    const messageElement = document.createElement("div");
    messageElement.className = "message-loading";
    messageElement.innerHTML = "AI가 고객님의 메시지를 분석중입니다 <div class='spinner-grow spinner-grow-sm' role='status'></div>";
    translationContent.appendChild(messageElement);
}

function removeAILoading() {
    const messageElement = document.querySelector(".message-loading");
    if (messageElement) {
        messageElement.remove();
    }
}

function endCounseling() {
    const userConfirmed = confirm("상담을 종료하시겠습니까?\n상담 종료시 대시보드로 이동합니다.");
    if (userConfirmed) {
        updateLog();
        window.location.href = "/";
    }
}