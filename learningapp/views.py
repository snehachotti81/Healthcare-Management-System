from django.shortcuts import render, redirect
from learningapp.forms import UserForm, UserProfileForm, UserUpdateForm, UserProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from doctors.models import Appointment

# Safely import Lab_Tech (may not exist yet)
try:
    from labReports.models import Lab_Tech, Lab_Tests
except ImportError:
    Lab_Tech = None
    Lab_Tests = None


def registration(request):
    registerd = False
    if request.method == "POST":
        form1 = UserForm(request.POST)
        form2 = UserProfileForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            profile = form2.save(commit=False)
            profile.user = user
            profile.save()
            registerd = True
    else:
        form1 = UserForm()
        form2 = UserProfileForm()
    context = {'form1': form1, 'form2': form2, 'registerd': registerd}
    return render(request, "registration.html", context)


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect("home")
            else:
                return HttpResponse("User is not active.")
        else:
            return HttpResponse("Invalid credentials. Please check your username and password.")

    return render(request, "login.html", {})


@login_required(login_url='login')
def home(request):
    """
    Home view — shows different content based on whether the user
    is a Lab Technician or a regular user (as designed on the whiteboard).
    """
    context = {'is_lab_tech': False}

    if Lab_Tech is not None:
        try:
            lab_tech = Lab_Tech.objects.get(user=request.user)
            context['is_lab_tech'] = True
            context['lab_tech'] = lab_tech
        except Lab_Tech.DoesNotExist:
            pass

    return render(request, "home.html", context)


@login_required(login_url='login')
def profile(request):
    appointments = Appointment.objects.filter(user=request.user).order_by('-date')
    return render(request, "profile.html", {'appointments': appointments})


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def update(request):
    if request.method == 'POST':
        form  = UserUpdateForm(request.POST, instance=request.user)
        form1 = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.userdetails)
        if form.is_valid() and form1.is_valid():
            user    = form.save()
            profile = form1.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('profile')
    else:
        form  = UserUpdateForm(instance=request.user)
        form1 = UserProfileUpdateForm(instance=request.user.userdetails)
    return render(request, "update.html", {'form': form, 'form1': form1})