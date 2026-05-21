from django.urls import path
from doctors import views


urlpatterns = [
    path('alldoctors',views.alldoctors,name="alldoctors"),
    path('treatments/', views.treatments_view, name='treatments'),
    path('doctors/',views.list_of_doctors,name='doctors'),
    path('book/<int:treatment_id>/', views.book_appointment, name='book_appointment'),
   
]
