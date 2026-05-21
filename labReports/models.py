from django.db import models
from django.contrib.auth.models import User
from learningapp.models import UserDetails
from doctors.models import ALLDOCTORS


# Create your models here.
class Lab_Tech(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    emp_id = models.PositiveIntegerField()
    Qualification = models.CharField(max_length=100)
    year_of_exp = models.PositiveIntegerField()
    address = models.CharField(max_length=200)


# All_lab_tests = [
#     ('CBC','cbc'),
#     ('LFT','lft'),
#     ('Urine Total Test','urine total test'),
#     ('Urine Microscopic','urine microscopic'),
#     ('Serum Routine','serum routine'),
#     ('Thyroid','thyroid')
# ]
All_lab_tests = [
    ('CBC', 'cbc'),
    ('LFT', 'lft'),
    ('KFT', 'kft'),
    ('RFT', 'rft'),
    ('Urine Total Test', 'urine total test'),
    ('Urine Microscopic', 'urine microscopic'),
    ('Serum Routine', 'serum routine'),
    ('Thyroid Profile (T3, T4, TSH)', 'thyroid'),
    
    # Diabetes Tests
    ('Fasting Blood Sugar (FBS)', 'fbs'),
    ('Postprandial Blood Sugar (PPBS)', 'ppbs'),
    ('HbA1c', 'hba1c'),

    # Lipid Profile
    ('Lipid Profile', 'lipid profile'),

    # Liver & Kidney
    ('Bilirubin Total/Direct', 'bilirubin'),
    ('Serum Creatinine', 'serum creatinine'),
    ('Blood Urea', 'blood urea'),

    # Electrolytes
    ('Sodium', 'sodium'),
    ('Potassium', 'potassium'),
    ('Chloride', 'chloride'),

    # Cardiac Tests
    ('Troponin I', 'troponin'),
    ('CK-MB', 'ckmb'),

    # Infection Tests
    ('Dengue Test', 'dengue'),
    ('Malaria Test', 'malaria'),
    ('COVID-19 RT-PCR', 'covid'),
    ('Widal Test', 'widal'),
    ('HIV Test', 'hiv'),
    ('HBsAg (Hepatitis B)', 'hbsag'),
    ('HCV (Hepatitis C)', 'hcv'),

    # Hormonal Tests
    ('Vitamin D', 'vitamin d'),
    ('Vitamin B12', 'vitamin b12'),
    ('Prolactin', 'prolactin'),
    ('Testosterone', 'testosterone'),
    ('Estrogen', 'estrogen'),

    # Coagulation Tests
    ('Prothrombin Time (PT)', 'pt'),
    ('INR', 'inr'),

    # Imaging (if your system supports it)
    ('X-Ray', 'xray'),
    ('Ultrasound (USG)', 'ultrasound'),
    ('CT Scan', 'ct scan'),
    ('MRI Scan', 'mri'),
]

test_result = [
    ('PENDING','pending'),
    ('ONGOING','ongoing'),
    ('COMPLETED','completed')
]

test_range = [
    ('NIL','nil'),
    ('POSITIVE','positive'),
    ('NEGATIVE','negative'),
    ('NORMAL','normal'),
    ('ABNORMAL','abnormal')
]

class Lab_Tests(models.Model):
    referred_by = models.ForeignKey(ALLDOCTORS,on_delete=models.CASCADE)
    patient_name = models.ForeignKey(UserDetails,on_delete=models.CASCADE)
    lab_test = models.CharField(max_length=100,choices=All_lab_tests)
    lab_result = models.CharField(max_length=100,choices=test_result)
    created_at = models.DateTimeField(auto_now_add=True)
    result_range = models.CharField(max_length=100,choices=test_range,default='nil')
    result_desc = models.TextField(blank=True, default='')
    test_cost = models.IntegerField()

    