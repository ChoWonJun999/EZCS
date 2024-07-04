function editCustomerInfo() {
    const form = document.getElementById('customer-form');
    const inputs = form.querySelectorAll('input');
    inputs.forEach(input => input.disabled = false);

    document.querySelector('.edit-button').style.display = 'none';
    document.querySelectorAll('.save-button, .cancel-button').forEach(button => {
        button.style.display = 'inline-block';
    });
}

function saveCustomerInfo() {
    const form = document.getElementById('customer-form');
    const inputs = form.querySelectorAll('input');
    inputs.forEach(input => input.disabled = true);

    // Add logic to save customer info, e.g., sending data to the server
    alert('고객 정보가 저장되었습니다.');

    document.querySelector('.edit-button').style.display = 'inline-block';
    document.querySelectorAll('.save-button, .cancel-button').forEach(button => {
        button.style.display = 'none';
    });
}

function cancelEdit() {
    const form = document.getElementById('customer-form');
    const inputs = form.querySelectorAll('input');
    inputs.forEach(input => input.disabled = true);

    // Add logic to handle canceling the edit, e.g., reverting changes
    alert('수정이 취소되었습니다.');

    document.querySelector('.edit-button').style.display = 'inline-block';
    document.querySelectorAll('.save-button, .cancel-button').forEach(button => {
        button.style.display = 'none';
    });
}

function editMemo() {
    const textarea = document.getElementById('memo-text');
    textarea.disabled = false;

    document.querySelector('.edit-button').style.display = 'none';
    document.querySelectorAll('.save-button, .cancel-button').forEach(button => {
        button.style.display = 'inline-block';
    });
}

function saveMemo() {
    const textarea = document.getElementById('memo-text');
    textarea.disabled = true;

    // Add logic to save memo content, e.g., sending data to the server
    alert('메모가 저장되었습니다.');

    document.querySelector('.edit-button').style.display = 'inline-block';
    document.querySelectorAll('.save-button, .cancel-button').forEach(button => {
        button.style.display = 'none';
    });
}

function cancelMemoEdit() {
    const textarea = document.getElementById('memo-text');
    textarea.disabled = true;

    // Add logic to handle canceling the memo edit, e.g., reverting changes
    alert('메모 수정이 취소되었습니다.');

    document.querySelector('.edit-button').style.display = 'inline-block';
    document.querySelectorAll('.save-button, .cancel-button').forEach(button => {
        button.style.display = 'none';
    });
}

function editConsultation() {
    const form = document.getElementById('consultation-form');
    const textareas = form.querySelectorAll('textarea');
    textareas.forEach(textarea => textarea.disabled = false);

    document.querySelector('.edit-button').style.display = 'none';
    document.querySelectorAll('.save-button, .cancel-button').forEach(button => {
        button.style.display = 'inline-block';
    });
}

function saveConsultation() {
    const form = document.getElementById('consultation-form');
    const textareas = form.querySelectorAll('textarea');
    textareas.forEach(textarea => textarea.disabled = true);

    // Add logic to save consultation info, e.g., sending data to the server
    alert('문의/조치 내용이 저장되었습니다.');

    document.querySelector('.edit-button').style.display = 'inline-block';
    document.querySelectorAll('.save-button, .cancel-button').forEach(button => {
        button.style.display = 'none';
    });
}

function cancelConsultationEdit() {
    const form = document.getElementById('consultation-form');
    const textareas = form.querySelectorAll('textarea');
    textareas.forEach(textarea => textarea.disabled = true);

    // Add logic to handle canceling the consultation edit, e.g., reverting changes
    alert('문의/조치 내용 수정이 취소되었습니다.');

    document.querySelector('.edit-button').style.display = 'inline-block';
    document.querySelectorAll('.save-button, .cancel-button').forEach(button => {
        button.style.display = 'none';
    });
}
