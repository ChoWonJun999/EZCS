document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("quiz-form");
    form.addEventListener("submit", function (event) {
        event.preventDefault(); // 폼 기본 제출 동작 방지

        const answers = [];
        const quizIds = [];

        // 단답형 및 객관식 답변 수집
        document.querySelectorAll('.answer-input').forEach(input => {
            answers.push(input.value);
            quizIds.push(input.name.split('_')[1]);
        });

        document.querySelectorAll('input[type="radio"]:checked').forEach(input => {
            answers.push(input.value);
            quizIds.push(input.name.split('_')[1]);
        });

        // 숨겨진 필드에 JSON 문자열 설정
        document.getElementById('id_answers').value = JSON.stringify(answers);
        document.getElementById('id_quiz_ids').value = JSON.stringify(quizIds);

        const formData = new FormData(form);

        fetch(form.action, {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": formData.get("csrfmiddlewaretoken")
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            const endButton = document.querySelector('.end-button');
            endButton.style.display = 'block';
            const submitButton = document.querySelector('.submit-button');
            submitButton.parentNode.removeChild(submitButton);
            return response.json(); // JSON 형식으로 응답을 처리
        })
        .then((data) => {
            // 결과를 처리하고 해설을 표시하는 코드
            if (data.results) {
                for (const [quizId, result] of Object.entries(data.results)) {
                    const feedback = document.getElementById(`feedback-${quizId}`);
                    const explanation = document.getElementById(`explanation-${quizId}`);
                    const correctAnswer = document.getElementById(`correct-answer-${quizId}`);
                    const input = document.getElementById(`input-${quizId}`);
                    if (feedback && explanation && correctAnswer) {
                        if (result.is_correct) {
                            feedback.innerHTML = '<span class="feedback-correct">정답입니다.</span>';
                        } else {
                            feedback.innerHTML = '<span class="feedback-incorrect">오답입니다!</span>';
                        }
                        if (input) {
                            input.setAttribute("readonly", true);
                        }
                        explanation.style.display = "block";
                        explanation.querySelector('.explanation-content').innerText = result.commentary || "해설 없음";
                        correctAnswer.style.display = "block";
                        correctAnswer.querySelector('.correct-answer-content').innerText = result.correct_answer || "정답 없음";
                    }
                }
            }
        })
        .catch((error) => {
            console.error('There was a problem with the fetch operation:', error);
        });
    });
});