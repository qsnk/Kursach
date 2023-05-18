from django.contrib import admin
from .models import Doctor, Record, Speciality, CustomUser

# Register your models here.

admin.site.register(Doctor)
admin.site.register(Record)
admin.site.register(Speciality)
admin.site.register(CustomUser)