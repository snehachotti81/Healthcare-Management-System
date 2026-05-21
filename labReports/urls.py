from django.urls import path
from labReports import views

urlpatterns = [
    path('LabTechReg/',                 views.LabTechReg,          name='LabTechReg'),
    path('all-tests/',                  views.all_tests,           name='all_tests'),
    path('dashboard/',                  views.lab_dashboard,       name='lab_dashboard'),
    path('update-result/<int:pk>/',     views.update_test_result,  name='update_test_result'),
    path('discharge/',                  views.discharge,           name='discharge'),
    path('discharge/receipt/<int:pk>/', views.discharge_receipt,   name='discharge_receipt'),
    path('all_lab_test',                views.add_lab_test,        name='all_lab_test'),
]