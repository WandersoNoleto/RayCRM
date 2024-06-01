from django.contrib import admin
from .models import Clinic, Receptionist, Doctor, PartnerOptic


admin.site.register(Clinic)
admin.site.register(Receptionist)
admin.site.register(PartnerOptic)
admin.site.register(Doctor)
