from django.contrib import admin
from .models import DischargeSummary, Payment


@admin.register(DischargeSummary)
class DischargeSummaryAdmin(admin.ModelAdmin):
    list_display  = ['patient_name', 'doctor', 'room_type', 'doa', 'dod', 'total_days', 'total_amount']
    list_filter   = ['room_type']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display  = ['discharge', 'amount_paid', 'payment_method', 'payment_status', 'paid_at']
    list_filter   = ['payment_status', 'payment_method']