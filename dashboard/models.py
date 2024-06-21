from django.db import models
from users.models import Clinic
from datetime import datetime, timedelta

class Patient(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    birth_date = models.DateField()
    address = models.CharField(max_length=255)
    last_appointment = models.DateField(null=True, blank=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def formatted_phone(self):
        phone = self.phone
        if len(phone) == 11:
            return f'({phone[:2]}) {phone[2:7]}-{phone[7:]}'
        else:
            return phone

    def __str__(self):
        return self.name
    
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    #TODO: Choices
    pay_method = models.CharField(max_length=50, default="n_atendido")

    def __str__(self):
        return f"Agendamento: {self.patient.name}, {self.appointment_date} às {self.appointment_time}"

class NextConsultDate(models.Model):
    date = models.DateField(default=datetime.now() + timedelta(days=20))

    def show(self):
        day = str(self.date.day).zfill(2)
        mon = str(self.date.month).zfill(2)

        
        return f"{day}/{mon}"

    def __str__(self):
        return str(self.date)
    

class PaymentMethods(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
