from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# specializations = [
#     ("GENERAL MEDICINE",'general medicine'),
#     ('CARDIOLOGIST','cardiologist'),
#     ('ENT','ent'),
#     ('ORTHOPENDIC','orthopendic'),
#     ('EYE SPECIALIST','eye specialist'),
#     ('DENTIST','dentist'),
#     ('OTHERS','others')
# ]
specializations = [
    ("general_medicine", "General Medicine"),
    ("cardiology", "Cardiologist"),
    ("ent", "ENT (Ear, Nose, Throat)"),
    ("orthopedic", "Orthopedic"),
    ("ophthalmology", "Eye Specialist"),
    ("dentistry", "Dentist"),
    ("dermatology", "Dermatologist"),
    ("pediatrics", "Pediatrician"),
    ("gynecology", "Gynecologist"),
    ("neurology", "Neurologist"),
    ("psychiatry", "Psychiatrist"),
    ("urology", "Urologist"),
    ("oncology", "Oncologist"),
    ("radiology", "Radiologist"),
    ("anesthesiology", "Anesthesiologist"),
    ("pulmonology", "Pulmonologist"),
    ("gastroenterology", "Gastroenterologist"),
    ("endocrinology", "Endocrinologist"),
    ("nephrology", "Nephrologist"),
    ("others", "Others"),
]

class ALLDOCTORS(models.Model):
    name = models.CharField(max_length=100)
    specialized = models.CharField(choices=specializations)
    yoe = models.IntegerField()
    Lic_no = models.CharField(max_length=100)
    certificate = models.ImageField(upload_to='certificates/',blank=True,null=True)
    age = models.PositiveIntegerField()
    email = models.EmailField()
    address = models.CharField(max_length=100)
    phone = models.BigIntegerField()

    def __str__(self):
        return self.name

# categories = [
#     ('DENTAL CARE','Dental Care'),
#     ('HEART CHECKUP','Heart Checkup'),
#     ('SKIN TREATMENT','Skin Treatment'),
#     ('EYE CHECKUP','Eye Checkup'),
#     ('ORTHOPEDIC CARE','Orthopedic Care'),
#     ('PHYSIOTHERAPY','Physiotherapy'),
#     ('GENERAL CHECKUP','General Checkup'),
#     ('ENT TREATMENT','ENT Treatment'),
#     ('DIABETES CARE','Diabetes Care')

# ]
categories = [
    ("dental_care", "Dental Care"),
    ("cardiology_checkup", "Heart Checkup"),
    ("skin_treatment", "Skin Treatment"),
    ("eye_checkup", "Eye Checkup"),
    ("orthopedic_care", "Orthopedic Care"),
    ("physiotherapy", "Physiotherapy"),
    ("general_checkup", "General Checkup"),
    ("ent_treatment", "ENT Treatment"),
    ("diabetes_care", "Diabetes Care"),

    # Added more relevant categories
    ("pediatric_care", "Pediatric Care"),
    ("gynecology_care", "Gynecology Care"),
    ("neurology_consultation", "Neurology Consultation"),
    ("psychiatry_services", "Mental Health / Psychiatry"),
    ("urology_services", "Urology Services"),
    ("cancer_screening", "Cancer Screening"),
    ("radiology_scan", "Radiology / Imaging"),
    ("lung_checkup", "Pulmonary / Lung Checkup"),
    ("digestive_health", "Gastroenterology"),
    ("hormone_disorders", "Endocrinology"),
    ("kidney_care", "Nephrology"),
    ("emergency_services", "Emergency Services"),
]

class Treatment(models.Model):
    treatment_name = models.CharField(choices=categories)
    category = models.CharField(choices=specializations)
    description = models.TextField()
    doctor_name = models.ForeignKey(ALLDOCTORS,on_delete=models.CASCADE)

    def __str__(self):
        return self.treatment_name

time_slots = [
    ('09:00 AM', '09:00 AM'),
    ('10:00 AM', '10:00 AM'),
    ('11:00 AM', '11:00 AM'),
    ('12:00 PM', '12:00 PM'),
    ('02:00 PM', '02:00 PM'),
    ('03:00 PM', '03:00 PM'),
    ('04:00 PM', '04:00 PM'),
]

gender_choices = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # ← add this
    doctorname = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    date = models.DateField()
    time = models.CharField(max_length=20, choices=time_slots)
    consultation_charges = models.CharField(max_length=100, default='550')
    patient_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=gender_choices)
    patient_email = models.EmailField()
    patient_phone = models.BigIntegerField()
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.patient_name


      
