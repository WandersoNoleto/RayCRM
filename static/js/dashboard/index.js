function searchAppointments() {
    const searchDate = document.getElementById('search-date').value;

    if (!searchDate) {
        alert('Por favor, insira uma data.');
        return;
    }

    axios.get(`/api/appointments?date=${searchDate}`)
        .then(response => {
            const appointments = response.data;
            const appointmentsBody = document.getElementById('appointmentsBody');
            const noAppointmentsRow = document.getElementById('noAppointmentsRow');

            // Clear previous appointments
            appointmentsBody.innerHTML = '';

            if (appointments.length === 0) {
                appointmentsBody.appendChild(noAppointmentsRow);
            } else {
                appointments.forEach(appointment => {
                    const row = document.createElement('tr');
                    const timeCell = document.createElement('td');
                    const patientCell = document.createElement('td');

                    timeCell.textContent = appointment.time;
                    patientCell.textContent = appointment.patient.name;

                    row.appendChild(timeCell);
                    row.appendChild(patientCell);
                    appointmentsBody.appendChild(row);
                });
            }
        })
        .catch(error => {
            console.error('There was an error fetching the appointments:', error);
        });
}

