from django.urls import path
from . import views

urlpatterns = [
    path('pay/<int:pk>/',      views.make_payment,   name='make_payment'),
    path('all-discharges/',    views.all_discharges, name='all_discharges'),
]