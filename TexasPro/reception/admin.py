from django.contrib import admin

# Register your models here.

from .models import user_details, doctor, queue, prescription
admin.site.register(user_details)
admin.site.register(doctor)
admin.site.register(queue)
admin.site.register(prescription)