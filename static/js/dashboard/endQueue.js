function updateButtonVisibility() {
    const nextButton = document.querySelector('.btn-next');
    const endQueueButton = document.querySelector('.btn-end-queue');
    console.log(waitingCount)
    if (waitingCount > 0) {
        nextButton.style.display = 'inline-block';
        endQueueButton.style.display = 'none';
    } else {
        nextButton.style.display = 'none';
        endQueueButton.style.display = 'flex';
    }
}


function finalizeQueue() {
    fetch('/finalize_queue/', {
        method: 'GET',
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Erro ao finalizar atendimento');
        }
    })
    .then(data => {
        openFinalizeQueueModal(data);
    })
    .catch(error => {
        console.error('Erro ao finalizar atendimento:', error);
        alert('Erro ao finalizar atendimento. Por favor, tente novamente.');
    });
}

function openFinalizeQueueModal(data) {
    document.getElementById('totalPatients').innerText = data.total_patients;

    const paymentMethodCounts = document.getElementById('paymentMethodCounts');
    paymentMethodCounts.innerHTML = '';
    
    for (const method in data.payment_method_counts) {
        const count = data.payment_method_counts[method];

        // Criando um parágrafo para cada método de pagamento
        const methodParagraph = document.createElement('p');
        methodParagraph.classList.add('font-weight-bold', 'text-center', 'end-queue-modal-stats');

        // Primeiro span com o nome do método de pagamento
        const methodNameSpan = document.createElement('span');
        methodNameSpan.innerText = method;
        methodParagraph.appendChild(methodNameSpan);

        // Segundo span com a quantidade de pacientes
        const countSpan = document.createElement('span');
        countSpan.id = `${method.replace(/\s+/g, '-').toLowerCase()}-count`; // ID baseado no nome do método
        countSpan.innerText = count;
        methodParagraph.appendChild(countSpan);

        paymentMethodCounts.appendChild(methodParagraph);
    }

    // Exibe o modal
    document.getElementById('endQueueModal').classList.remove('hidden');
}


function openEndQueueModal() {
    const modal = document.getElementById('endQueueModal');
    modal.classList.remove('hidden');
}

// Função para fechar o modal
function closeEndQueueModal() {
    const modal = document.getElementById('endQueueModal');
    modal.classList.add('hidden');
}