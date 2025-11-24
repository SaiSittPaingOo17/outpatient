from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'patient',
        'appointment',
        'total_amount',
        'amount_paid',
        'payment_method',
        'status',
        'created_at',
    )
    list_filter = ('status', 'payment_method',)
    search_fields = ('patient__fname', 'patient__lname', 'appointment__id')
