from django.urls import path
from . import views

app_name = 'payment'
urlpatterns = [
    path('pay/<int:payment_id>/', views.make_payment, name='make_payment'),
    path('invoice/<int:payment_id>/', views.payment_invoice_pdf, name='payment_invoice'),
    path('success/<int:payment_id>/', views.payment_success, name='payment_success'),
    path('invoice/<int:payment_id>/', views.payment_invoice_pdf, name='payment_invoice'),

]