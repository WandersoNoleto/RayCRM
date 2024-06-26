let currentAppointmentIndex = -1; 
const totalAppointmentsElement = document.getElementById('total-appointments');
const treatedCountElement = document.getElementById('treated-count');
const waitingCountElement = document.getElementById('waiting-count');

const totalAppointments = parseInt(totalAppointmentsElement.innerText);
let treatedCount = 0-1;
let waitingCount = totalAppointments+1;

document.getElementById('treated-count').innerText = treatedCount;
document.getElementById('waiting-count').innerText = waitingCount;

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

            treatedCount++;
            waitingCount--;

            treatedCountElement.innerText = treatedCount;
            waitingCountElement.innerText = waitingCount;
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
    const idInput = document.getElementById('appointment-id');
    const nameInput = document.getElementById('name');
    const birthDateInput = document.getElementById('birth-date');
    const phoneInput = document.getElementById('phone');
    const paymentMethodSelect = document.getElementById('payment-method');
    const saveButton = document.getElementById('btn-save');

    if (patientData) {
        idInput.value = patientData.id;
        nameInput.value = patientData.name;
        birthDateInput.value = patientData.birth_date;
        phoneInput.value = patientData.phone;
        paymentMethodSelect.value = patientData.payment_method;

        paymentMethodSelect.disabled = false;
        saveButton.disabled = false;

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


document.getElementById('appointment-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);

    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao atualizar os dados do paciente.');
        }
        return response.json();
    })
    .then(data => {
        const paymentMethodSelect = document.getElementById('payment-method');
        const selectedPaymentMethodId = formData.get('payment-method');
        const option = paymentMethodSelect.querySelector(`option[value="${selectedPaymentMethodId}"]`);
        if (option) {
            option.selected = true;

            const currentPaymentMethodElement = document.querySelector('.current-payment-method');
            if (currentPaymentMethodElement) {
                currentPaymentMethodElement.textContent = option.textContent.trim();
            }
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao atualizar os dados do paciente.');
    });
});

