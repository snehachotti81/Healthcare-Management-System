from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from labReports.forms import LabTechRegistrationForm, LabTestForm
from labReports.models import Lab_Tech, Lab_Tests, All_lab_tests
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404


def LabTechReg(request):
    if request.method == 'POST':
        form = LabTechRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Lab_Tech.objects.create(
                user          = user,
                emp_id        = form.cleaned_data['emp_id'],
                Qualification = form.cleaned_data['Qualification'],
                year_of_exp   = form.cleaned_data['year_of_exp'],
                address       = form.cleaned_data['address'],
            )
            messages.success(request, f'Account created for {user.username}! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LabTechRegistrationForm()

    return render(request, "LabReports/LabTechReg.html", {'form': form})


@login_required(login_url='login')
def all_tests(request):
    price_map = {
        'CBC': 350,
        'LFT': 600,
        'KFT': 550,
        'RFT': 550,
        'Urine Total Test': 200,
        'Urine Microscopic': 250,
        'Serum Routine': 450,
        'Thyroid Profile (T3, T4, TSH)': 800,
        'Fasting Blood Sugar (FBS)': 150,
        'Postprandial Blood Sugar (PPBS)': 150,
        'HbA1c': 500,
        'Lipid Profile': 700,
        'Bilirubin Total/Direct': 300,
        'Serum Creatinine': 200,
        'Blood Urea': 180,
        'Sodium': 150,
        'Potassium': 150,
        'Chloride': 150,
        'Troponin I': 900,
        'CK-MB': 750,
        'Dengue Test': 900,
        'Malaria Test': 300,
        'COVID-19 RT-PCR': 1200,
        'Widal Test': 250,
        'HIV Test': 500,
        'HBsAg (Hepatitis B)': 400,
        'HCV (Hepatitis C)': 600,
        'Vitamin D': 1200,
        'Vitamin B12': 800,
        'Prolactin': 600,
        'Testosterone': 900,
        'Estrogen': 900,
        'Prothrombin Time (PT)': 300,
        'INR': 250,
        'X-Ray': 500,
        'Ultrasound (USG)': 1200,
        'CT Scan': 4000,
        'MRI Scan': 7000,
    }

    time_map = {
        'CBC': '6-8 hrs',
        'LFT': '12-24 hrs',
        'KFT': '12-24 hrs',
        'RFT': '12-24 hrs',
        'Urine Total Test': '4-6 hrs',
        'Urine Microscopic': '6-8 hrs',
        'Serum Routine': '12-24 hrs',
        'Thyroid Profile (T3, T4, TSH)': '24-48 hrs',
        'Fasting Blood Sugar (FBS)': '4-6 hrs',
        'Postprandial Blood Sugar (PPBS)': '4-6 hrs',
        'HbA1c': '24 hrs',
        'Lipid Profile': '12-24 hrs',
        'Bilirubin Total/Direct': '12 hrs',
        'Serum Creatinine': '6-8 hrs',
        'Blood Urea': '6-8 hrs',
        'Sodium': '4-6 hrs',
        'Potassium': '4-6 hrs',
        'Chloride': '4-6 hrs',
        'Troponin I': '6 hrs',
        'CK-MB': '6-8 hrs',
        'Dengue Test': '24 hrs',
        'Malaria Test': '6-8 hrs',
        'COVID-19 RT-PCR': '24-48 hrs',
        'Widal Test': '12 hrs',
        'HIV Test': '24 hrs',
        'HBsAg (Hepatitis B)': '24 hrs',
        'HCV (Hepatitis C)': '24-48 hrs',
        'Vitamin D': '24-48 hrs',
        'Vitamin B12': '24 hrs',
        'Prolactin': '24 hrs',
        'Testosterone': '24-48 hrs',
        'Estrogen': '24-48 hrs',
        'Prothrombin Time (PT)': '6 hrs',
        'INR': '6 hrs',
        'X-Ray': '1-2 hrs',
        'Ultrasound (USG)': '2-4 hrs',
        'CT Scan': '6-12 hrs',
        'MRI Scan': '12-24 hrs',
    }

    # 1. Build the full list FIRST
    tests = [
        {
            'code':  code,
            'name':  code,
            'price': price_map.get(code, 'N/A'),
            'time':  time_map.get(code, '24-48 hrs'),
        }
        for code, label in All_lab_tests
    ]

    # 2. THEN paginate
    paginator   = Paginator(tests, 7)
    page_number = request.GET.get('pg')
    tests_page  = paginator.get_page(page_number)

    return render(request, "LabReports/pk_doctor.html", {'tests': tests_page})


@login_required(login_url='login')
def lab_dashboard(request):
    try:
        Lab_Tech.objects.get(user=request.user)
    except Lab_Tech.DoesNotExist:
        messages.error(request, "Access restricted to Lab Technicians only.")
        return redirect('home')

    lab_tests = Lab_Tests.objects.select_related(
        'referred_by',
        'patient_name',
        'patient_name__user',
    ).order_by('created_at')

    total_tests     = lab_tests.count()
    pending_count   = lab_tests.filter(lab_result='PENDING').count()
    ongoing_count   = lab_tests.filter(lab_result='ONGOING').count()
    completed_count = lab_tests.filter(lab_result='COMPLETED').count()

    paginator   = Paginator(lab_tests, 3)
    page_number = request.GET.get('pg')
    lab_tests   = paginator.get_page(page_number)

    context = {
        'lab_tests':       lab_tests,
        'total_tests':     total_tests,
        'pending_count':   pending_count,
        'ongoing_count':   ongoing_count,
        'completed_count': completed_count,
    }
    return render(request, "LabReports/dashboard.html", context)


@login_required(login_url='login')
def update_test_result(request, pk):
    try:
        record = Lab_Tests.objects.select_related(
            'referred_by', 'patient_name', 'patient_name__user'
        ).get(pk=pk)
    except Lab_Tests.DoesNotExist:
        messages.error(request, "Test record not found.")
        return redirect('lab_dashboard')

    if request.method == 'POST':
        lab_result   = request.POST.get('lab_result')
        result_range = request.POST.get('result_range')
        result_desc  = request.POST.get('result_desc', '')

        if lab_result:
            record.lab_result = lab_result
        if result_range:
            record.result_range = result_range
        record.result_desc = result_desc
        record.save()

        messages.success(request, "Test result updated successfully.")
        return redirect('lab_dashboard')

    return render(request, "LabReports/update_result.html", {'record': record})


@login_required(login_url='login')
def discharge(request):
    return render(request, "LabReports/discharge.html", {})


@login_required(login_url='login')
def add_lab_test(request):
    form = LabTestForm()
    if request.method == 'POST':
        form = LabTestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lab_dashboard')
    return render(request, 'LabReports/add_lab_test.html', {'form': form})
@login_required(login_url='login')
def discharge(request):
    from payment.forms import DischargeSummaryForm
    from labReports.models import Lab_Tests

    form = DischargeSummaryForm()

    if request.method == 'POST':
        form = DischargeSummaryForm(request.POST)
        if form.is_valid():
            summary           = form.save(commit=False)
            patient           = form.cleaned_data['patient_name']
            lab_tests         = Lab_Tests.objects.filter(patient_name=patient)
            summary.lab_charges = sum(t.test_cost for t in lab_tests)
            summary.save()
            messages.success(request, "Discharge completed! Proceed to payment.")
            return redirect('make_payment', pk=summary.pk)
        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, "LabReports/discharge.html", {'form': form})


@login_required(login_url='login')
def discharge_receipt(request, pk):
    from payment.models import DischargeSummary, Payment
    from labReports.models import Lab_Tests

    summary   = get_object_or_404(DischargeSummary, pk=pk)
    lab_tests = Lab_Tests.objects.filter(patient_name=summary.patient_name)
    payment   = Payment.objects.filter(discharge=summary).first()

    return render(request, "LabReports/discharge_receipt.html", {
        'summary':   summary,
        'lab_tests': lab_tests,
        'payment':   payment,
    })