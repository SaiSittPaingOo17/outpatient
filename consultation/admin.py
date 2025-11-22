from django.contrib import admin
from .models import PrescriptionType, Prescription

# Register your models here.
class PrescriptionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'prescription_type', 'created_at', 'updated_at')
    list_filter = ('prescription_type',)
    search_fields = ('prescription_type',)

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'consultation_id','prescription','created_at')
    list_filter = ('prescription',)
    search_fields = ('prescription_type',)

admin.site.register(PrescriptionType, PrescriptionTypeAdmin)
admin.site.register(Prescription, PrescriptionAdmin)