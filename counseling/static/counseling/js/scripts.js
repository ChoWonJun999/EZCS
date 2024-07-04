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
    alert('고객 정보가 저장되었습니다.');

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
    alert('수정이 취소되었습니다.');

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
    alert('메모가 저장되었습니다.');

    document.querySelector('#memo-form .edit-button').style.display = 'inline-block';
    document.querySelectorAll('#memo-form .save-button, #memo-form .cancel-button').forEach(button => {
        button.style.display = 'none';
    });
}

function cancelMemoEdit() {
    const textarea = document.getElementById('memo-text');
    textarea.disabled = true;

    // 메모 수정 취소를 처리하는 로직 추가, 예: 변경 사항 되돌리기
    alert('메모 수정이 취소되었습니다.');

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
    alert('문의/조치 내용이 저장되었습니다.');

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
    alert('문의/조치 내용 수정이 취소되었습니다.');

    document.querySelector('#consultation-form .edit-button').style.display = 'inline-block';
    document.querySelectorAll('#consultation-form .save-button, #consultation-form .cancel-button').forEach(button => {
        button.style.display = 'none';
    });
}
