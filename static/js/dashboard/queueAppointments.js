let currentAppointmentIndex = -1; 
const totalAppointmentsElement = document.getElementById('total-appointments');
const treatedCountElement = document.getElementById('treated-count');
const waitingCountElement = document.getElementById('waiting-count');

const totalAppointments = parseInt(totalAppointmentsElement.innerText);
let treatedCount = 0-1;
let waitingCount = totalAppointments+1;

document.getElementById('treated-count').innerText = treatedCount;
document.getElementById('waiting-count').innerText = waitingCount;

// JavaScript (frontend)

function startConsultationDay() {
    document.getElementById('normalContent').classList.add('hidden');
    document.getElementById('diaDeConsultaContent').classList.remove('hidden');

    var novaAlturaEm = 38.1;
    var novaAlturaPixels = novaAlturaEm * 16;
    document.getElementById('tableContainer').style.maxHeight = novaAlturaPixels + 'px';

    // Marca a fila como iniciada no backend
    fetch('/start_queue/', {
        method: 'GET',
    })
    .then(response => {
        if (response.ok) {
            console.log('Fila iniciada com sucesso');
        } else {
            console.error('Erro ao iniciar a fila:', response.status);
        }
    })
    .catch(error => {
        console.error('Erro ao iniciar a fila:', error);
    });

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
                fetch(`/update_last_treated_appointment/${appointmentId}/`, {
                    method: 'GET',
                })
                .then(response => {
                    if (response.ok) {
                        console.log(`Último agendamento tratado atualizado: ${appointmentId}`);
                    } else {
                        console.error('Erro ao atualizar o último agendamento tratado:', response.status);
                    }
                })
                .catch(error => {
                    console.error('Erro ao atualizar o último agendamento tratado:', error);
                });
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
    updateButtonVisibility()
}


function startHighlightFromAppointment(startAppointmentId) {
    const appointmentRows = document.querySelectorAll('tr[id^="appointment-"]');
    let found = false;
    let appointmentsAfter = 0;

    for (let i = 0; i < appointmentRows.length; i++) {
        const appointmentId = appointmentRows[i].getAttribute('data-appointment-id');
        if (appointmentId && parseInt(appointmentId) === startAppointmentId) {
            appointmentRows[i].classList.add('current-patient');
            fetchPatientData(appointmentId);
            currentAppointmentIndex = i;
            found = true;
            appointmentRows[i].scrollIntoView({ behavior: 'smooth', block: 'center' });
            for (let j = i + 1; j < appointmentRows.length; j++) {
                const filledCell = appointmentRows[j].querySelector('.filled-cell');
                if (filledCell) {
                    appointmentsAfter++;
                }
            }

            break;
        }
    }

    if (!found) {
        currentAppointmentIndex = -1;
    }

    let totalAppointmentsWithFilledCells = 0;
    for (let i = 0; i < appointmentRows.length; i++) {
        if (appointmentRows[i].querySelector('.filled-cell')) {
            totalAppointmentsWithFilledCells++;
        }
    }

    treatedCount = totalAppointmentsWithFilledCells - appointmentsAfter;  
    waitingCount = appointmentsAfter; 

    treatedCountElement.innerText = treatedCount;
    waitingCountElement.innerText = waitingCount;

    var novaAlturaEm = 38.1;
    var novaAlturaPixels = novaAlturaEm * 16;

    document.getElementById('tableContainer').style.maxHeight = novaAlturaPixels + 'px';
    updateButtonVisibility()
}



function goToNextAppointment() {
    highlightNextAppointment();
}



