document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('quiz-form');
    form.addEventListener('submit', function (event) {
        event.preventDefault();  // 폼 기본 제출 동작 방지

        const formData = new FormData(form);
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            // 결과를 처리하고 해설을 표시하는 코드
            if (data.results) {
                for (const [quizId, result] of Object.entries(data.results)) {
                    const feedback = document.getElementById(`feedback-${quizId}`);
                    const explanation = document.getElementById(`explanation-${quizId}`);
                    const input = document.getElementById(`input-${quizId}`);
                    if (feedback && explanation) {
                        if (result.is_correct) {
                            feedback.innerHTML = '<span class="feedback-correct">정답입니다.</span>';
                        } else {
                            feedback.innerHTML = '<span class="feedback-incorrect">오답입니다!</span>';
                        }
                        if (input) {
                            input.setAttribute('readonly', true);
                        }
                        explanation.style.display = 'block';
                    }
                }
            }
        });
    });
});
