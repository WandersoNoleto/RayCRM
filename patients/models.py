from django.db import models
from users.models import Clinic
import re
from datetime import date
  
class Patient(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    birth_date = models.DateField()
    address = models.CharField(max_length=255)
    last_appointment = models.DateField(null=True, blank=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def calculate_age(self):
        today = date.today()
        age = today.year - self.birth_date.year
        
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        
        return age

    def formatted_phone(self):
        phone = re.sub(r'\D', '', self.phone)
        
        if len(phone) == 9:
            return f'{phone[:5]}-{phone[5:]}'
        else:
            return f'({phone[:2]}) {phone[2:7]}-{phone[7:]}'

    def __str__(self):
        return self.name

