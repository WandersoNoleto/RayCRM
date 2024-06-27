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

async function showCancelAlert(appointmentId) {
    new window.Swal({
        icon: 'warning',
        title: 'Tem certeza que quer desmarcar este agendamento?',
        showCancelButton: true,
        cancelButtonText: 'Não',
        confirmButtonText: 'Sim',
        padding: '2em',
    }).then((result) => {
        if (result.value) {
            fetch(`/appointments/cancel/${appointmentId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                }
            }).then(response => {
                if (response.ok) {
                    window.location.reload();
                    
                } else {
                    console.error('Erro ao cancelar agendamento:', response.statusText);
                }
            }).catch(error => {
                console.error('Erro ao cancelar agendamento:', error);
            });
        }
    });

    window.onload = function() {
        const urlParams = new URLSearchParams(window.location.search);
        const successMessage = urlParams.get('success_message');
        if (successMessage === 'appointment_cancelled') {
            const alertElement = document.createElement('div');
            alertElement.className = 'success-alert';
            alertElement.textContent = 'Agendamento cancelado com sucesso!';
            document.body.appendChild(alertElement);
    
            // Remover a mensagem após alguns segundos
            setTimeout(() => {
                alertElement.remove();
            }, 5000);
        }
    };
}

window.onload = function() {
    var messageContainer = document.getElementById('messageContainer');
    if (messageContainer) {
        setTimeout(function() {
            messageContainer.style.display = 'none';
        }, 5000);
    }
};

document.getElementById('submitAppointmentForm').addEventListener('click', function(event) {
    var dateInput = document.getElementById('dateStart').value;
    var date = new Date(dateInput);

    fetch('/get_next_consult_date/')
        .then(response => response.json())
        .then(data => {
            var nextConsultDate = new Date(data.next_consult_date);

            if (date.getDay() !== 2 && date !== nextConsultDate) {
                Swal.fire({
                    icon: 'warning',
                    title: 'A data informada não é uma quarta-feira',
                    text: 'Você deseja continuar com esta data?',
                    showCancelButton: true,
                    confirmButtonText: 'Sim',
                    cancelButtonText: 'Não'
                }).then((result) => {
                    if (result.isConfirmed) {
                        document.getElementById('appointmentForm').submit();
                    }
                });
            } else {
                document.getElementById('appointmentForm').submit();
            }
        })
        .catch(error => {
            console.error('Erro ao obter a próxima data de consulta:', error);
            // Adicione uma mensagem de erro se necessário
        });
});


document.getElementById('submitEditNextConsultDateForm').addEventListener('click', function(event) {
    var dateInput = document.getElementById('nextConsultDate').value;
    var date = new Date(dateInput);

    if (date.getDay() !== 2) {
        Swal.fire({
            icon: 'warning',
            title: 'A data informada não é uma quarta-feira',
            text: 'Você deseja continuar com esta data?',
            showCancelButton: true,
            confirmButtonText: 'Sim',
            cancelButtonText: 'Não'
        }).then((result) => {
            if (result.isConfirmed) {
                document.getElementById('editNextConsultDateForm').submit();
            }
        });
    } else {
        document.getElementById('editNextConsultDateForm').submit();
    }
});

