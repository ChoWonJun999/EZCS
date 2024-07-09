document.addEventListener('DOMContentLoaded', function () {
    // 고객 정보 폼
    document.getElementById('customer-form').addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            saveCustomerInfo();
        }
    });

    // 메모 폼
    document.getElementById('memo-form').addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            saveMemo();
        }
    });

    // 문의/조치 내용 폼
    document.getElementById('consultation-form').addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            saveConsultation();
        }
    });
});

function editCustomerInfo() {
    const form = document.getElementById('customer-form');
    const inputs = form.querySelectorAll('input:not([type="button"])');
    inputs.forEach(input => input.disabled = false);

    form.querySelector('.edit-button').style.display = 'none';
    form.querySelectorAll('.save-button, .cancel-button').forEach(button => {
        button.style.display = 'inline-block';
    });
}

function saveCustomerInfo() {
    const form = document.getElementById('customer-form');
    const inputs = form.querySelectorAll('input:not([type="button"])');

    // 고객 정보를 저장하는 로직 추가, 예: 서버로 데이터 전송
    const phoneInput = document.getElementById('phone');
    if (phoneInput.value.length !== 11 || !/^\d{11}$/.test(phoneInput.value)) {
        alert('전화번호는 11자리 숫자여야 합니다.');
        phoneInput.disabled = false; // 입력 필드 다시 활성화
        return;
    }
    
    const formData = new FormData(form);
    fetch('/counseling/save_customer_info/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('고객 정보가 저장되었습니다.');
            } else {
                alert('고객 정보 저장에 실패했습니다.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('고객 정보 저장 중 오류가 발생했습니다.');
        });

    inputs.forEach(input => input.disabled = true);
    form.querySelector('.edit-button').style.display = 'inline-block';
    form.querySelectorAll('.save-button, .cancel-button').forEach(button => {
        button.style.display = 'none';
    });
}

function cancelEdit() {
    const form = document.getElementById('customer-form');
    const inputs = form.querySelectorAll('input:not([type="button"])');
    inputs.forEach(input => input.disabled = true);

    // 수정 취소를 처리하는 로직 추가, 예: 변경 사항 되돌리기
    // alert('수정이 취소되었습니다.');

    form.querySelector('.edit-button').style.display = 'inline-block';
    form.querySelectorAll('.save-button, .cancel-button').forEach(button => {
        button.style.display = 'none';
    });
}

function editMemo() {
    const textarea = document.getElementById('memo-text');
    textarea.disabled = false;

    document.querySelector('#memo-form .edit-button').style.display = 'none';
    document.querySelectorAll('#memo-form .save-button, #memo-form .cancel-button').forEach(button => {
        button.style.display = 'inline-block';
    });
}

function saveMemo() {
    const textarea = document.getElementById('memo-text');
    textarea.disabled = true;

    // 메모 내용을 저장하는 로직 추가, 예: 서버로 데이터 전송
    // alert('메모가 저장되었습니다.');

    document.querySelector('#memo-form .edit-button').style.display = 'inline-block';
    document.querySelectorAll('#memo-form .save-button, #memo-form .cancel-button').forEach(button => {
        button.style.display = 'none';
    });
}

function cancelMemoEdit() {
    const textarea = document.getElementById('memo-text');
    textarea.disabled = true;

    // 메모 수정 취소를 처리하는 로직 추가, 예: 변경 사항 되돌리기
    // alert('메모 수정이 취소되었습니다.');

    document.querySelector('#memo-form .edit-button').style.display = 'inline-block';
    document.querySelectorAll('#memo-form .save-button, #memo-form .cancel-button').forEach(button => {
        button.style.display = 'none';
    });
}

function editConsultation() {
    const form = document.getElementById('consultation-form');
    const textareas = form.querySelectorAll('textarea');
    textareas.forEach(textarea => textarea.disabled = false);

    document.querySelector('#consultation-form .edit-button').style.display = 'none';
    document.querySelectorAll('#consultation-form .save-button, #consultation-form .cancel-button').forEach(button => {
        button.style.display = 'inline-block';
    });
}

function saveConsultation() {
    const form = document.getElementById('consultation-form');
    const textareas = form.querySelectorAll('textarea');
    textareas.forEach(textarea => textarea.disabled = true);

    // 문의/조치 내용을 저장하는 로직 추가, 예: 서버로 데이터 전송
    // alert('문의/조치 내용이 저장되었습니다.');

    document.querySelector('#consultation-form .edit-button').style.display = 'inline-block';
    document.querySelectorAll('#consultation-form .save-button, #consultation-form .cancel-button').forEach(button => {
        button.style.display = 'none';
    });
}

function cancelConsultationEdit() {
    const form = document.getElementById('consultation-form');
    const textareas = form.querySelectorAll('textarea');
    textareas.forEach(textarea => textarea.disabled = true);

    // 문의/조치 내용 수정 취소를 처리하는 로직 추가, 예: 변경 사항 되돌리기
    // alert('문의/조치 내용 수정이 취소되었습니다.');

    document.querySelector('#consultation-form .edit-button').style.display = 'inline-block';
    document.querySelectorAll('#consultation-form .save-button, #consultation-form .cancel-button').forEach(button => {
        button.style.display = 'none';
    });
}

const transcription = document.getElementById('transcription');
const customerStartButton = document.getElementById('customer-start-button');
const counselorStartButton = document.getElementById('counselor-start-button');
const stopButton = document.getElementById('stop-button');
const saveButton = document.getElementById('save-button');
const translationContent = document.getElementById('translation-content');
let mediaRecorder;
let audioChunks = [];
let currentTranscriptionDiv;
let recognition;
let currentStream;
let audioBlob;

// 기본 메시지 저장
const defaultTranscriptionMessage = transcription.innerHTML;

function startCustomerCounseling() {
    startCounseling('customer');
}

function startCounselorCounseling() {
    startCounseling('counselor');
}

function startCounseling(type) {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = 'ko-KR';
            let finalTranscript = '';

            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            currentStream = stream;

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.start();

            removeExistingInterimDiv();

            // 기본 메시지 숨기기
            transcription.innerHTML = '';

            currentTranscriptionDiv = document.createElement('div');
            currentTranscriptionDiv.className = 'interim-msg';
            if (type === 'customer') {
                currentTranscriptionDiv.innerHTML = '<strong>고객:</strong> ';
            } else {
                currentTranscriptionDiv.innerHTML = '<strong>상담원:</strong> ';
            }
            transcription.appendChild(currentTranscriptionDiv);

            recognition.onstart = () => {
                if (type === 'customer') {
                    customerStartButton.disabled = true;
                } else {
                    counselorStartButton.disabled = true;
                }
                stopButton.disabled = false;
                console.log('Counseling started');
            };

            recognition.onresult = event => {
                let interimTranscript = '';
                const results = event.results;

                for (let i = event.resultIndex; i < results.length; i++) {
                    if (results[i].isFinal) {
                        finalTranscript += results[i][0].transcript + ' ';
                    } else {
                        interimTranscript += results[i][0].transcript;
                    }
                }

                currentTranscriptionDiv.innerHTML = (type === 'customer' ? '<strong>고객:</strong> ' : '<strong>상담원:</strong> ') + finalTranscript + interimTranscript;
            };

            recognition.onerror = event => {
                console.error('Speech recognition error:', event.error);
                if (type === 'customer') {
                    customerStartButton.disabled = false;
                } else {
                    counselorStartButton.disabled = false;
                }
                stopButton.disabled = true;
            };

            recognition.onend = () => {
                if (type === 'customer') {
                    customerStartButton.disabled = false;
                } else {
                    counselorStartButton.disabled = false;
                }
                stopButton.disabled = true;
                saveButton.disabled = false;
                console.log('Counseling ended');

                if (finalTranscript.trim() !== '') {
                    const finalDiv = createFinalDiv(finalTranscript, type);
                    transcription.appendChild(finalDiv);
                    if (type === 'customer') {
                        sendTextToChatbot(finalTranscript);
                        addCustomerMessageToTranslationContent(finalTranscript);
                    }
                }

                currentTranscriptionDiv.remove();
                mediaRecorder.stop();

                // 기본 메시지를 다시 표시
                if (transcription.innerHTML.trim() === '') {
                    transcription.innerHTML = defaultTranscriptionMessage;
                }
            };

            recognition.start();

            window.recognition = recognition;
            window.audioStream = stream;
        })
        .catch(error => {
            console.error('Error accessing media devices.', error);
        });
}

function stopCounseling() {
    if (recognition) {
        recognition.stop();
    }

    if (currentStream) {
        currentStream.getTracks().forEach(track => track.stop());
    }

    customerStartButton.disabled = false;
    counselorStartButton.disabled = false;
    stopButton.disabled = true;

    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        mediaRecorder.onstop = () => {
            audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        };
    }
}

function removeExistingInterimDiv() {
    const existingInterimDiv = document.querySelector('.interim-msg');
    if (existingInterimDiv) {
        existingInterimDiv.remove();
    }
}

function createFinalDiv(text, type) {
    const finalDiv = document.createElement('div');
    finalDiv.className = `output-msg ${type}`;
    finalDiv.innerHTML = (type === 'customer' ? '<strong>고객:</strong> ' : '<strong>상담원:</strong> ') + text;
    return finalDiv;
}

function sendTextToChatbot(text) {
    const formData = new FormData();
    formData.append('text', text);
    formData.append('username', '홍길동');
    
    fetch('/counseling/stt_chat/', {
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
                childDiv.className = 'chatbot-response';
                childDiv.innerText = data.output;
                translationContent.appendChild(childDiv);
            } else if (data.error) {
                console.error('Error from server:', data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function addCustomerMessageToTranslationContent(text) {
    const translationDiv = document.createElement('div');
    translationDiv.className = 'output-msg customer';
    translationDiv.innerHTML = '<strong>고객:</strong> ' + text;
    translationContent.appendChild(translationDiv);
}

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
    formData.append('audio', audioBlob, 'recording.webm');
    
    fetch('/counseling/save_audio/', {
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
        alert('파일이 성공적으로 저장되었습니다.');
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

saveButton.addEventListener('click', saveRecording);


// 텍스트 데이터를 챗봇에 전송하는 함수(view.py에 전송)
function sendTextToChatbot(text) {
    const formData = new FormData();
    formData.append('text', text);
    // DB 저장을 위한 데이터(미완성)
    formData.append('username', '홍길동')
    
    fetch('/counseling/stt_chat/', {
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
                childDiv.className = 'chatbot-response';
                childDiv.innerText = data.output;
                translationContent.appendChild(childDiv);  // 챗봇 응답을 translation-content div에 추가
            } else if (data.error) {
                console.error('Error from server:', data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// 오디오 데이터를 서버로 전송하는 함수(임시로 로컬로 저장하게 구현)
function sendAudioToServer(audioBlob) {
    const url = URL.createObjectURL(audioBlob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = 'recording.webm';  // 파일명 설정
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

// CSRF 토큰을 가져오는 함수
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
