function openAddModal() {
    document.getElementById('patient-form').reset();
    document.getElementById('patientId').value = '';
    document.getElementById('modalTitle').innerText = 'Adicionar Paciente';
    document.querySelector('#patientModal button[type="submit"]').innerText = 'Adicionar';
    document.getElementById('patientModal').style.display = 'block';
}

function openEditModal(patient) {
    document.getElementById('patientId').value = patient.id;
    document.getElementById('name').value = patient.name;
    document.getElementById('birth_date').value = patient.birth_date;
    document.getElementById('phone').value = patient.phone;
    document.getElementById('address').value = patient.address;
    document.getElementById('modalTitle').innerText = 'Editar Paciente';
    document.querySelector('#patientModal button[type="submit"]').innerText = 'Salvar';
    document.getElementById('patientModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('patientModal').style.display = 'none';
}

function editPatient(id) {
    fetch(`get/${id}/`)
        .then(response => response.json())
        .then(data => {
            openEditModal(data);
        });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getCSRFToken() {
    return getCookie('csrftoken');
}

function savePatient(event) {
    event.preventDefault();

    const patientId = document.getElementById('patientId').value;
    const url = patientId ? `edit/${patientId}/` : `add/`;
    const method = patientId ? 'PUT' : 'POST';

    const patientData = {
        name: document.getElementById('name').value,
        birth_date: document.getElementById('birth_date').value,
        phone: document.getElementById('phone').value,
        address: document.getElementById('address').value
    };

    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify(patientData)
    }).then(response => {
        if (response.ok) {
            closeModal();
            window.location.reload();
        }
    });
}

async function showDeleteAlert(patientName, patientId) {
    new window.Swal({
        icon: 'warning',
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        showCancelButton: true,
        confirmButtonText: 'Delete',
        padding: '2em',
    }).then((result) => {
        if (result.value) {
            fetch(`delete/${patientId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                }
            }).then(response => {
                if (response.ok) {
                    window.location.reload();
                } else {
                    console.error('Error deleting patient:', response.statusText);
                }
            }).catch(error => {
                console.error('Error deleting patient:', error);
            });
        }
    });
    
}