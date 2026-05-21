from django.contrib import admin
from labReports.models import Lab_Tech, Lab_Tests

# Register your models here.
admin.site.register(Lab_Tests)
admin.site.register(Lab_Tech)