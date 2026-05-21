from django.db import models
from learningapp.models import UserDetails
from doctors.models import ALLDOCTORS

ROOM_TYPE_CHOICES = [
    ('common_ward',   'Common Ward'),
    ('semi_pvt',      'Semi-Private'),
    ('private_ac',    'Private AC'),
    ('private_nonac', 'Private Non-AC'),
    ('delux',         'Delux'),
]

ROOM_RATES = {
    'common_ward':   900,
    'semi_pvt':      2800,
    'private_ac':    3750,
    'private_nonac': 3350,
    'delux':         4850,
}

MEDICINE_PERCENT = {
    'common_ward':   10,
    'semi_pvt':      12,
    'private_ac':    15,
    'private_nonac': 13,
    'delux':         20,
}

PAYMENT_METHOD_CHOICES = [
    ('cash',   'Cash'),
    ('card',   'Card'),
    ('upi',    'UPI'),
    ('online', 'Online Banking'),
]

PAYMENT_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('paid',    'Paid'),
]


class DischargeSummary(models.Model):
    patient_name = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    doctor       = models.ForeignKey(ALLDOCTORS, on_delete=models.CASCADE)
    treatment    = models.CharField(max_length=200)
    description  = models.TextField(blank=True)
    doa          = models.DateField(verbose_name="Date of Admission")
    dod          = models.DateField(verbose_name="Date of Discharge")
    room_type    = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    total_days   = models.PositiveIntegerField()

    # Food as individual booleans
    food_morning    = models.BooleanField(default=False)
    food_lunch      = models.BooleanField(default=False)
    food_dinner     = models.BooleanField(default=False)
    food_coffee_tea = models.BooleanField(default=False)

    # Computed fields — auto filled on save
    room_charges     = models.IntegerField(default=0)
    medicine_charges = models.IntegerField(default=0)
    food_charges     = models.IntegerField(default=0)
    lab_charges      = models.IntegerField(default=0)
    total_amount     = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        days = self.total_days
        self.room_charges     = ROOM_RATES.get(self.room_type, 0) * days
        pct                   = MEDICINE_PERCENT.get(self.room_type, 0)
        self.medicine_charges = int(self.room_charges * pct / 100)

        food_per_day = 0
        if self.food_morning:    food_per_day += 120
        if self.food_lunch:      food_per_day += 200
        if self.food_dinner:     food_per_day += 160
        if self.food_coffee_tea: food_per_day += 40
        self.food_charges = food_per_day * days

        self.total_amount = (
            self.room_charges + self.medicine_charges +
            self.food_charges + self.lab_charges
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Discharge - {self.patient_name} ({self.dod})"


class Payment(models.Model):
    discharge      = models.OneToOneField(DischargeSummary, on_delete=models.CASCADE, related_name='payment')
    amount_paid    = models.IntegerField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    paid_at        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment - {self.discharge.patient_name} - {self.payment_status}"