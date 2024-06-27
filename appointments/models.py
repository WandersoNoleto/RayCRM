from django.db import models
from patients.models import Patient
   
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    payment_method = models.ForeignKey('dashboard.PaymentMethods', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Agendamento: {self.patient.name}, {self.date} às {self.time}"
    
class ConsultationDaySummary(models.Model):
    consultation_date = models.DateField()
    total_patients = models.IntegerField()
    payment_method_counts = models.JSONField()  

    def __str__(self):
        return f"Consultation Summary for {self.consultation_date}"
