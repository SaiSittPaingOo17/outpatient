# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from consultation.models import Consultation
# from .models import Payment

# @receiver(post_save, sender=Consultation)
# def create_payment_on_consultation(sender, instance, created, **kwargs):
#     if created:
#         # Create payment skeleton for this visit
#         Payment.objects.create(
#             patient=instance.appointment.patient,
#             appointment=instance.appointment,
#             consultation=instance,
#             total_amount=0,  
#             amount_paid=0,
#             status="unpaid"
#         )
