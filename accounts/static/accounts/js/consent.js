$(document).ready(function () {
    const form = $('#consentForm');
    const checkAll = $('#checkAll');
    const checkBoxes = $('input[name="agreement"]');
    const submitButton = $('input[type="submit"]');

    const agreements = {
        termsOfService: false,
        privacyPolicy: false,
        allowPromotions: false,
    };

    checkBoxes.on('change', function () {
        const id = $(this).attr('id');
        agreements[id] = $(this).prop('checked');
        toggleCheckboxClass(this);
        checkAll.prop('checked', areAllChecked());
        toggleSubmitButton();
    });

    function toggleCheckboxClass(checkbox) {
        const isChecked = $(checkbox).prop('checked');
        $(checkbox).closest('.input_check').toggleClass('active', isChecked);
    }

    function areAllChecked() {
        return Object.values(agreements).every(val => val);
    }

    function toggleSubmitButton() {
        submitButton.prop('disabled', !agreements.termsOfService || !agreements.privacyPolicy);
    }

    checkAll.on('change', function () {
        const isChecked = $(this).prop('checked');
        checkBoxes.prop('checked', isChecked).each(function () {
            const id = $(this).attr('id');
            agreements[id] = isChecked;
            toggleCheckboxClass(this);
        });
        toggleSubmitButton();
    });
});
