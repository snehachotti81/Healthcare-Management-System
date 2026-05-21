from django.shortcuts import render, get_object_or_404, redirect
from .models import Treatment, ALLDOCTORS, Appointment
from django.contrib.auth.models import User
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required


def alldoctors(request):
    doctors = ALLDOCTORS.objects.all()
    return render(request, "doctors/alldoctors.html", {'doctors': doctors})


def treatments_view(request):
    treatments = Treatment.objects.all()
    return render(request, 'doctors/treatments.html', {'treatments': treatments})


def list_of_doctors(request):
    treatment = Treatment.objects.all()
    return render(request, "doctors/list_of_doctors.html", {'treatment': treatment})


# @login_required(login_url='login')
def book_appointment(request, treatment_id):
    treatment = get_object_or_404(Treatment, id=treatment_id)

    initial_data = {
        'doctorname': treatment.doctor_name.name,
        'category': treatment.category,
        'consultation_charges': '1000',
    }

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user        # ← link to logged-in user
            appointment.consultation_charges = '1000'
            appointment.category = treatment.category
            appointment.save()
            return redirect('doctors')
        else:
            print("Form errors:", form.errors)
    else:
        form = AppointmentForm(initial=initial_data)

    return render(request, "doctors/appointment.html", {'form': form, 'treatment': treatment})