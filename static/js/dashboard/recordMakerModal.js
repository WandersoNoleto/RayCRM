document.addEventListener('DOMContentLoaded', function() {
    const documentFreeLink = document.getElementById('free-doc');
    const addDocumentModal = document.getElementById('addDocumentModal');
    console.log(documentFreeLink)
    if (documentFreeLink && addDocumentModal) {
        documentFreeLink.addEventListener('click', function(event) {
            event.preventDefault(); // Evita o comportamento padrão do link
            addDocumentModal.classList.remove('hidden');
        });
    }

    document.getElementById('addDocumentForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Evita o envio padrão do formulário

        const fileName = document.getElementById('fileName').value;
        const fileContent = document.getElementById('fileContent').value;

        fetch('/create-pdf/', { // Substitua '/create-pdf/' pela URL correta da sua view
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
            },
            body: JSON.stringify({
                file_name: fileName,
                file_content: fileContent,
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                closeModal();
                alert('Documento criado com sucesso!');
            } else {
                alert('Erro ao criar o documento: ' + data.error);
            }
        })
        .catch(error => console.error('Erro na requisição:', error));
    });
});

function closeModal() {
    document.getElementById('addDocumentModal').classList.add('hidden');
}
