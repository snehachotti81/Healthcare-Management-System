from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import DischargeSummary, Payment
from .forms import PaymentForm


@login_required(login_url='login')
def make_payment(request, pk):
    summary = get_object_or_404(DischargeSummary, pk=pk)

    # if already paid, go straight to receipt
    if hasattr(summary, 'payment') and summary.payment.payment_status == 'paid':
        return redirect('discharge_receipt', pk=pk)

    form = PaymentForm()

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.discharge      = summary
            payment.amount_paid    = summary.total_amount
            payment.payment_status = 'paid'
            payment.save()
            messages.success(request, "Payment successful!")
            return redirect('discharge_receipt', pk=pk)

    return render(request, 'payment/make_payment.html', {
        'summary': summary,
        'form':    form,
    })


@login_required(login_url='login')
def all_discharges(request):
    discharges = DischargeSummary.objects.all().order_by('-created_at')
    return render(request, 'payment/all_discharges.html', {'discharges': discharges})