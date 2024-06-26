from django.db import models
from users.models import Clinic
from datetime import datetime, timedelta
  
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
    

