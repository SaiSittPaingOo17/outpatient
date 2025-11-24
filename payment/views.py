from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

from .models import Payment
from .forms import PaymentForm

def make_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    # Get prescriptions for display
    medication_list = payment.consultation.prescription_set.filter(
        prescription_type__prescription_type='medication'
    )

    test_list = payment.consultation.prescription_set.filter(
        prescription_type__prescription_type='laboratory'
    )

    if request.method == "POST":
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():

            payment = form.save(commit=False)
            payment.manual_recalculate_total()

            if payment.amount_paid >= payment.total_amount:
                payment.status = 'paid'
            else:
                payment.status = 'partial'

            payment.save()

            return redirect("payment:payment_success", payment.id)

    else:
        form = PaymentForm(instance=payment)

    return render(request, "payment/make_payment.html", {
        "payment": payment,
        "form": form,
        "medications": medication_list,
        "tests": test_list,
    })


def payment_invoice_pdf(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    template_path = 'payment/invoice.html'
    context = {'payment': payment}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{payment.id}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    return response

def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, "payment/payment_success.html", {"payment": payment})
