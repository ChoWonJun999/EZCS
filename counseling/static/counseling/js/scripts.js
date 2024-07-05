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
    inputs.forEach(input => input.disabled = true);

    // 고객 정보를 저장하는 로직 추가, 예: 서버로 데이터 전송
    // alert('고객 정보가 저장되었습니다.');

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
const startButton = document.getElementById('start-button');
const stopButton = document.getElementById('stop-button');
const recommendedAnswer = document.querySelector('.recommended-answer');
let mediaRecorder;
let audioChunks = [];

// 상담 시작 함수
function startCounseling() {
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
            transcription.appendChild(interimDiv);

            // 음성 인식 시작 시 버튼 비활성화 및 로그 출력
            recognition.onstart = () => {
                startButton.disabled = true;
                stopButton.disabled = false;
                console.log('Counseling started');
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
                console.log('Counseling ended');

                if (finalTranscript.trim() !== '') {
                    const finalDiv = createFinalDiv(finalTranscript);
                    transcription.appendChild(finalDiv);
                    sendTextToChatbot(finalTranscript);  // 텍스트 데이터를 챗봇에 전송
                }

                interimDiv.remove();
                mediaRecorder.stop(); // 음성 녹음 중지
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

// 상담 종료 함수
function stopCounseling() {
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
            // const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            sendAudioToServer(audioBlob);
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
    finalDiv.className = 'output-msg';
    finalDiv.innerText = text;
    return finalDiv;
}

// 텍스트 데이터를 챗봇에 전송하는 함수(view.py에 전송)
function sendTextToChatbot(text) {
    const formData = new FormData();
    formData.append('text', text);

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
                recommendedAnswer.appendChild(childDiv);  // 챗봇 응답을 recommended-answer div에 추가
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
    // const formData = new FormData();
    // formData.append('audio', audioBlob);

    // fetch('/counseling/stt_audio/', {
    //     method: 'POST',
    //     body: formData,
    //     headers: {
    //         'X-CSRFToken': getCookie('csrftoken')
    //     }
    // })
    // .then(response => {
    //     if (!response.ok) {
    //         throw new Error('Network response was not ok');
    //     }
    //     return response.json();
    // })
    // .then(data => {
    //     console.log('Audio data sent to server:', data);
    // })
    // .catch(error => {
    //     console.error('Error:', error);
    // });
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
