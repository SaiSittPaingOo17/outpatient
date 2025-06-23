from django.contrib import admin
from .models import Patient, Doctor, Appointment, Department

# Register your models here.
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone")
    def name(self, obj):
        return obj.pat_name

    def phone(self, obj):
        return obj.pat_phone

class DoctorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "department")

    def name(self, obj):
        return obj.doc_name
    def department(self, obj):
        return obj.doc_dep


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Appointment)
admin.site.register(Department)