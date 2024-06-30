function showPatientData(appointmentId) {
    let patientData = fetchPatientData(appointmentId);
    updatePatientPanel(patientData);
}


function updatePatientPanel(patientData) {
    const idInput = document.getElementById('appointment-id');
    const nameInput = document.getElementById('name');
    const birthDateInput = document.getElementById('birth-date');
    const phoneInput = document.getElementById('phone');
    const paymentMethodSelect = document.getElementById('payment-method');
    const saveButton = document.getElementById('btn-save');
    const deleteButton = document.getElementById('btn-delete-appointment');

    if (patientData) {
        idInput.value = patientData.id;
        nameInput.value = patientData.name;
        birthDateInput.value = patientData.birth_date;
        phoneInput.value = patientData.phone;
        paymentMethodSelect.value = patientData.payment_method;

        paymentMethodSelect.disabled = false;
        saveButton.disabled = false;
        deleteButton.disabled = false;

        const paymentMethodId = patientData.payment_method;
        if (paymentMethodId) {
            const option = paymentMethodSelect.querySelector(`option[value="${paymentMethodId}"]`);
            if (option) {
                option.selected = true;
            }
        }
    } else {
        nameInput.value = '';
        birthDateInput.value = '';
        phoneInput.value = '';
        paymentMethodSelect.value = '';

        nameInput.disabled = true;
        birthDateInput.disabled = true;
        phoneInput.disabled = true;
        paymentMethodSelect.disabled = true;
        saveButton.disabled = true;
    }
}

function fetchPatientData(appointmentId) {
    fetch(`/appointments/get/${appointmentId}/`)
        .then(response => response.json())
        .then(data => {
            updatePatientPanel(data);
        })
        .catch(error => console.error('Error:', error));
}