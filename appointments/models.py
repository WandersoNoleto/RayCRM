from django.db import models
from patients.models import Patient
   
class Appointment(models.Model):
    APPOINTMENT_TYPE_CHOICES = [
        ('Consulta', 'Consulta'),
        ('Retorno', 'Retorno'),
    ]

    STATUS_CHOICES = [
        ('attended', 'Attended'),
        ('waiting', 'Waiting'),
        ('missed', 'Missed'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    type = models.CharField(max_length=10, choices=APPOINTMENT_TYPE_CHOICES, default='Consulta')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    payment_method = models.ForeignKey('dashboard.PaymentMethods', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Agendamento: {self.patient.name}, {self.date} às {self.time}"
    
class ConsultationDaySummary(models.Model):
    consultation_date = models.DateField()
    total_patients = models.IntegerField()
    payment_method_counts = models.JSONField()  

    def __str__(self):
        return f"Consultation Summary for {self.consultation_date}"
