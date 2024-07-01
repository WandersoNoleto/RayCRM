from django.db import models
from appointments.models import Appointment
  
class PaymentMethods(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class NextConsultDate(models.Model):
    date = models.DateField()

    def show(self):
        day = str(self.date.day).zfill(2)
        mon = str(self.date.month).zfill(2)

        
        return f"{day}/{mon}"

    def __str__(self):
        return str(self.date)


class QueueState(models.Model):
    is_started = models.BooleanField(default=False)
    last_treated_appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    total = models.IntegerField(default=0)
    consultations = models.IntegerField(default=0)
    follow_ups = models.IntegerField(default=0)
    attendeds = models.IntegerField(default=0)
    waiting = models.IntegerField(default=0)
    misseds = models.IntegerField(default=0)

    def __str__(self):
        return f"Queue State - Started: {self.is_started}"
    

