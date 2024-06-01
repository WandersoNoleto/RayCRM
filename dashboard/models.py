from django.db import models
from users.models import Clinic

class Patient(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
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