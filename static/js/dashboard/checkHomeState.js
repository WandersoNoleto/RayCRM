document.addEventListener('DOMContentLoaded', function() {
    fetch('/check_queue_state/')
        .then(response => response.json())
        .then(data => {
            if (data.is_started == true && data.last_treated_appointment) {
                document.getElementById('normalContent').classList.add('hidden');
                document.getElementById('diaDeConsultaContent').classList.remove('hidden');
                startHighlightFromAppointment(data.last_treated_appointment.id);

                const lastAppointmentName = data.last_treated_appointment.patient_name;
                document.getElementById('lastAppointmentName').innerText = lastAppointmentName;
            } else {
                document.getElementById('normalContent').classList.remove('hidden');
                document.getElementById('diaDeConsultaContent').classList.add('hidden');
            }
        })
        .catch(error => {
            console.error('Erro ao obter o estado da fila:', error);
        });
    });