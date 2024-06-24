function startConsultationDay() {
    document.getElementById('normalContent').classList.add('hidden');
    document.getElementById('diaDeConsultaContent').classList.remove('hidden');

    var novaAlturaEm = 38.1;
    var novaAlturaPixels = novaAlturaEm * 16;

    document.getElementById('tableContainer').style.maxHeight = novaAlturaPixels + 'px';
}

function closeConsultationDay() {
    document.getElementById('diaDeConsultaContent').classList.add('hidden');
    document.getElementById('normalContent').classList.remove('hidden');
}
