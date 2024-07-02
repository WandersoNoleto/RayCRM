from django.db import models
from django.utils import timezone
from patients.models import Patient

class MedicalRecord(models.Model):
    file_name = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()  
    file_path = models.FileField(upload_to='medical_records/')
    date_added = models.DateTimeField(default=timezone.now)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')

    def __str__(self):
        return self.file_name