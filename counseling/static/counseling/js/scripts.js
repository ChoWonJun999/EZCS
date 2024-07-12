const phoneInput = document.getElementById("phone");
const transcription = document.getElementById("transcription");
const customerStartButton = document.getElementById("customer-start-button");
const counselorStartButton = document.getElementById("counselor-start-button");
const stopButton = document.getElementById("stop-button");
const saveButton = document.getElementById("save-button");
const translationContent = document.getElementById("translation-content");
let mediaRecorder;
let audioChunks = [];
let recognition;
let currentStream;
let audioBlob;
let currentInterimDiv; // 현재 interim 메시지 div

document.addEventListener("DOMContentLoaded", function () {
    // 고객 정보 폼
    document.getElementById("customer-form").addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            saveCustomerInfo();
        }
    });

    // 메모 폼
    document.getElementById("memo-form").addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            saveMemo();
        }
    });

    // 문의/조치 내용 폼
    document.getElementById("consultation-form").addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            saveConsultation();
        }
    });
});

function editCustomerInfo() {
    const form = document.getElementById("customer-form");
    const inputs = form.querySelectorAll('input:not([type="button"])');
    inputs.forEach((input) => (input.disabled = false));

    form.querySelector(".edit-button").style.display = "none";
    form.querySelectorAll(".save-button, .cancel-button").forEach((button) => {
        button.style.display = "inline-block";
    });
}

function saveCustomerInfo() {
    const form = document.getElementById("customer-form");
    const inputs = form.querySelectorAll('input:not([type="button"])');

    // 고객 정보를 저장하는 로직 추가, 예: 서버로 데이터 전송
    if (phoneInput.value.length !== 11 || !/^\d{11}$/.test(phoneInput.value)) {
        alert("전화번호는 11자리 숫자여야 합니다.");
        phoneInput.disabled = false; // 입력 필드 다시 활성화
        return;
    }

    const formData = new FormData(form);
    fetch("/counseling/save_customer_info/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
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

function editMemo() {
    const textarea = document.getElementById("memo-text");
    textarea.disabled = false;

    document.querySelector("#memo-form .edit-button").style.display = "none";
    document.querySelectorAll("#memo-form .save-button, #memo-form .cancel-button").forEach((button) => {
        button.style.display = "inline-block";
    });
}

function saveMemo() {
    const textarea = document.getElementById("memo-text");
    textarea.disabled = true;

    // 메모 내용을 저장하는 로직 추가, 예: 서버로 데이터 전송
    // alert('메모가 저장되었습니다.');

    document.querySelector("#memo-form .edit-button").style.display = "inline-block";
    document.querySelectorAll("#memo-form .save-button, #memo-form .cancel-button").forEach((button) => {
        button.style.display = "none";
    });
}

function cancelMemoEdit() {
    const textarea = document.getElementById("memo-text");
    textarea.disabled = true;

    // 메모 수정 취소를 처리하는 로직 추가, 예: 변경 사항 되돌리기
    // alert('메모 수정이 취소되었습니다.');

    document.querySelector("#memo-form .edit-button").style.display = "inline-block";
    document.querySelectorAll("#memo-form .save-button, #memo-form .cancel-button").forEach((button) => {
        button.style.display = "none";
    });
}

function editConsultation() {
    const form = document.getElementById('consultation-form');
    const inquiryTextareas = form.querySelectorAll('textarea[name="inquiry-text"]');
    const actionTextareas = form.querySelectorAll('textarea[name="action-text"]');

    inquiryTextareas.forEach((textarea) => (textarea.disabled = false));
    actionTextareas.forEach((textarea) => (textarea.disabled = false));

    document.querySelector("#consultation-form .edit-button").style.display = "none";
    document.querySelectorAll("#consultation-form .save-button, #consultation-form .cancel-button").forEach((button) => {
        button.style.display = "inline-block";
    });
}

function saveConsultation() {

    const form = document.getElementById("consultation-form");
    const inquiryTextareas = form.querySelectorAll('textarea[name="inquiry-text"]');
    const actionTextareas = form.querySelectorAll('textarea[name="action-text"]');

    inquiryTextareas.forEach((textarea) => {
        const logId = textarea.getAttribute("data-log-id");
        const inquiryText = textarea.value;

        const actionTextarea = form.querySelector(`textarea[name="action-text"][data-log-id="${logId}"]`);
        const actionText = actionTextarea ? actionTextarea.value : "";

        const formData = new FormData();
        formData.append("log_id", logId);
        formData.append("inquiry_text", inquiryText);
        formData.append("action_text", actionText);

        fetch("/counseling/save_consultation/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    alert("문의 내용이 저장되었습니다.");
                    textarea.disabled = true;
                    if (actionTextarea) actionTextarea.disabled = true;
                    document.querySelector("#consultation-form .edit-button").style.display = "inline-block";
                    document.querySelectorAll("#consultation-form .save-button, #consultation-form .cancel-button").forEach((button) => {
                        button.style.display = "none";
                    });
                } else {
                    alert("문의 내용 저장에 실패했습니다.");
                    console.error("Error:", data.error); // 에러 메시지 출력
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("문의 내용 저장 중 오류가 발생했습니다.");
            });
    });
}

function cancelConsultationEdit() {

    const form = document.getElementById("consultation-form");
    const inquiryTextareas = form.querySelectorAll('textarea[name="inquiry-text"]');
    const actionTextareas = form.querySelectorAll('textarea[name="action-text"]');

    inquiryTextareas.forEach((textarea) => (textarea.disabled = true));
    actionTextareas.forEach((textarea) => (textarea.disabled = true));

    document.querySelector("#consultation-form .edit-button").style.display = "inline-block";
    document.querySelectorAll("#consultation-form .save-button, #consultation-form .cancel-button").forEach((button) => {
        button.style.display = "none";
    });
}

// 기본 메시지 저장
const defaultTranscriptionMessage = transcription.innerHTML;

function startCustomerCounseling() {
    startCounseling("customer");
}

function startCounselorCounseling() {
    startCounseling("counselor");
}

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
                if (type === "customer") {
                    customerStartButton.disabled = true;
                } else {
                    counselorStartButton.disabled = true;
                }
                stopButton.disabled = false;
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
                if (type === "customer") {
                    customerStartButton.disabled = false;
                } else {
                    counselorStartButton.disabled = false;
                }
                stopButton.disabled = true;
            };

            recognition.onend = () => {
                if (type === "customer") {
                    customerStartButton.disabled = false;
                } else {
                    counselorStartButton.disabled = false;
                }
                stopButton.disabled = true;
                saveButton.disabled = false;
                console.log("Counseling ended");

                if (finalTranscript.trim() !== "") {
                    const finalDiv = createFinalDiv(finalTranscript, type);
                    transcription.appendChild(finalDiv);
                    if (type === 'customer') {
                        evaluationTextToChatbot(finalTranscript);
                        addCustomerMessageToTranslationContent(finalTranscript);
                    }
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

    customerStartButton.disabled = false;
    counselorStartButton.disabled = false;
    stopButton.disabled = true;

    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
        mediaRecorder.onstop = () => {
            audioBlob = new Blob(audioChunks, { type: "audio/webm" });
        };
    }
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

    const phoneInput = document.getElementById("phone");
    const phone_number = phoneInput.value;

    // 전화번호 유효성 검사
    if (phoneInput.value.length !== 11 || !/^\d{11}$/.test(phoneInput.value)) {
        alert("고객의 전화번호를 입력하여주세요.");
        phoneInput.disabled = false; // 입력 필드 다시 활성화
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

    // CSRF 토큰 가져오기
    const csrftoken = getCookie("csrftoken");

    // 상담 로그 데이터 서버로 전송
    fetch("/counseling/save_counseling_log/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
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

// 파일 저장은 임시로 사용하지 않음
function saveRecording() {
    if (!audioBlob) {
        alert("녹음된 파일이 없습니다.");
        return;
    }

    const userConfirmed = confirm("파일을 저장하시겠습니까?");
    if (userConfirmed) {
        sendAudioToServer(audioBlob);
    }
}

function sendAudioToServer(audioBlob) {
    const formData = new FormData();
    formData.append("audio", audioBlob, "recording.webm");

    fetch("/counseling/save_audio/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then((data) => {
            alert("파일이 성공적으로 저장되었습니다.");
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}

function scrollToBottom() {
    transcription.scrollTop = transcription.scrollHeight;
}

// 텍스트 데이터를 챗봇에 전송하는 함수(view.py에 전송)
function evaluationTextToChatbot(text) {

    console.log("Sending text to chatbot:", text); // 로그 추가

    const formData = new FormData();
    formData.append("text", text);

    fetch("/counseling/evaluation_chat/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })

        .then((response) => {
            console.log(response); // 응답 로그 추가
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then((data) => {
            if (data.output) {
                const childDiv = document.createElement("div");
                childDiv.className = "chatbot-response";
                childDiv.innerText = data.output;
                translationContent.appendChild(childDiv); // 챗봇 응답을 translation-content div에 추가
            } else if (data.error) {
                console.error("Error from server:", data.error);
            }
        })
        .catch((error) => {
            console.error("Error:", error); // 오류 로그 추가
        });
}

// 오디오 데이터를 서버로 전송하는 함수(임시로 로컬로 저장하게 구현)
function sendAudioToServer(audioBlob) {
    const url = URL.createObjectURL(audioBlob);
    const a = document.createElement("a");
    a.style.display = "none";
    a.href = url;
    a.download = "recording.webm"; // 파일명 설정
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

// CSRF 토큰을 가져오는 함수
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
