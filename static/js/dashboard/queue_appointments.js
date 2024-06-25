function startConsultationDay() {
    document.getElementById('normalContent').classList.add('hidden');
    document.getElementById('diaDeConsultaContent').classList.remove('hidden');

    var novaAlturaEm = 38.1;
    var novaAlturaPixels = novaAlturaEm * 16;

    document.getElementById('tableContainer').style.maxHeight = novaAlturaPixels + 'px';

    highlightNextAppointment();
}

function closeConsultationDay() {
    document.getElementById('diaDeConsultaContent').classList.add('hidden');
    document.getElementById('normalContent').classList.remove('hidden');
}

let currentAppointmentIndex = -1; 

function highlightNextAppointment() {
    const appointmentRows = document.querySelectorAll('tr[id^="appointment-"]');
    let found = false;

    if (currentAppointmentIndex >= 0) {
        appointmentRows[currentAppointmentIndex].classList.remove('current-patient');
    }

    for (let i = currentAppointmentIndex + 1; i < appointmentRows.length; i++) {
        if (appointmentRows[i].querySelector('.filled-cell')) {
            appointmentRows[i].classList.add('current-patient');
            currentAppointmentIndex = i;
            found = true;

            const appointmentId = appointmentRows[i].getAttribute('data-appointment-id');
            if (appointmentId) {
                fetchPatientData(appointmentId);
            }

            appointmentRows[i].scrollIntoView({ behavior: 'smooth', block: 'center' });
            break;
        }
    }

    if (!found) {
        currentAppointmentIndex = -1;
    }
}

function goToNextAppointment() {
    highlightNextAppointment();
}

function showPatientData(appointmentId) {
    let patientData = fetchPatientData(appointmentId);
    updatePatientPanel(patientData);
}


function updatePatientPanel(patientData) {
    const nameInput = document.getElementById('name');
    const birthDateInput = document.getElementById('birth-date');
    const phoneInput = document.getElementById('phone');
    const paymentMethodSelect = document.getElementById('payment-method');
    const saveButton = document.getElementById('btn-save');

    if (patientData) {
        nameInput.value = patientData.name;
        birthDateInput.value = patientData.birth_date;
        phoneInput.value = patientData.phone;
        paymentMethodSelect.value = patientData.payment_method;

        nameInput.disabled = false;
        birthDateInput.disabled = false;
        phoneInput.disabled = false;
        paymentMethodSelect.disabled = false;
        saveButton.disabled = false;
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

function savePatientData() {
    const nameInput = document.getElementById('name');
    const birthDateInput = document.getElementById('birth-date');
    const phoneInput = document.getElementById('phone');
    const paymentMethodSelect = document.getElementById('payment-method');

    const patientData = {
        name: nameInput.value,
        birth_date: birthDateInput.value,
        phone: phoneInput.value,
        payment_method: paymentMethodSelect.value
    };

    fetch(`/api/save-patient-data/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(patientData)
    })
        .then(response => response.json())
        .then(data => {
            alert('Dados salvos com sucesso!');
        })
        .catch(error => console.error('Error:', error));
}
