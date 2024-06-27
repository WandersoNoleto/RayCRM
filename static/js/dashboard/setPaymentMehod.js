
document.getElementById('appointment-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);
    const appointmentId = formData.get('appointment_id');

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

            const appointmentRow = document.querySelector(`tr[data-appointment-id="${appointmentId}"]`);
            const currentPaymentMethodElement = appointmentRow.querySelector('.current-payment-method');
            if (currentPaymentMethodElement) {
                currentPaymentMethodElement.textContent = option.textContent.trim();
            }
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro:', error);
    });
});