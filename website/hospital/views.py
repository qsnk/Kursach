from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Patient, Doctor,Record, CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import PatientForm, LoginForm, RecordForm, RegistrationForm, MyDataEditForm #CreateUserForm
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import xlwt

# Create your views here.

def index(request):
    return render(request, 'index.html')

def contacts(request):
    return render(request, 'contacts.html')

def sign_in(request):
    form = LoginForm()
    context = {"form": form}
    if request.user.is_authenticated:
        return redirect('personal_account')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email = request.POST.get('email')
                password = request.POST.get("password")
                user = authenticate(email=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('personal_account')
                else:
                    messages.info(request, "Неверное имя пользователя или пароль!")
        return render(request, 'login.html', context)

@login_required(login_url='login')
def personal_account(request):
    if request.user.is_authenticated:
        records = Record.objects.filter(patient=request.user)
        context = {'records':records}
        return render(request, 'personal_account.html', context)
    else:
        return redirect('login')

@login_required(login_url='login')
def make_record(request):
    form = RecordForm()
    context = {'form':form}
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=request.user)
        date = request.POST.get('date')
        time = request.POST.get('rec_time')
        doc_id = request.POST.get('doctors_name')
        doc_name = Doctor.objects.get(pk=doc_id)
        patient = request.user
        description = request.POST.get('description')
        record = Record.create(date, time, doc_name, patient, description)
        record.save()
        return redirect('personal_account')
    return render(request, 'account/make_record.html', context)

@login_required(login_url='login')
def get_data(request):
    return render(request, 'account/my_data.html')

@login_required(login_url='login')
def edit_data(request):
    form = MyDataEditForm(instance=request.user)
    context = {"form": form}
    if request.method == 'POST':
        form = MyDataEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.info(request, 'Данные успешно обновлены, обновите страницу!')
        else:
            for field in form:
                print("Field Error:", field.name, field.errors)
                messages.info(request, field.errors)
    return render(request, 'account/edit.html', context)

def log_out(request):
    logout(request)
    return redirect('login')

def sign_up(request):
    if request.user.is_authenticated:
        return redirect('personal_account')
    else:
        form = PatientForm()
        context = {"form": form}
        if request.method == 'POST':
            form = PatientForm(request.POST)
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if CustomUser.objects.filter(email=email).exists():
                messages.info(request, "Такая электронная почта уже существует!")
            else:
                if form.is_valid():
                    if password1 == password2:
                        user = CustomUser.objects.create_user(email=email, username=username, password=password1)
                        user.save()
                        return redirect('login')
                    else:
                        messages.info(request, "Пароли не совпадают!")
                else:
                    for field in form:
                        print("Field Error:", field.name, field.errors)
                        messages.info(request, field.errors)
        return render(request, 'signup.html', context)

def about(request):
    return render(request, 'about.html')

def faq(request):
    return render(request, 'FAQ.html')

def news(request):
    return render(request, 'news.html')

@login_required(login_url='login')
def export_page(request):
    if request.user.is_authenticated:
        return render(request, 'account/export.html')
    else:
        return redirect('login')


def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Имя пользователя', 'Электронная почта', 'Имя', 'Фамилия', 'Отчество']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = CustomUser.objects.all().values_list('username',  'email', 'first_name', 'second_name', 'last_name',)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_doctors_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Doctors.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Doctors')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Имя', 'Фамилия', 'Отчество', 'Пол', 'Дата рождения', 'Электронная почта', 'Имя пользователя', 'Адрес', 'Телефон', 'Код специальности']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Doctor.objects.all().values_list('first_name', 'second_name', 'last_name', 'gender', 'birth_date', 'email', 'username', 'address', 'phone', 'speciality_id')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_records_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Records.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Дата', 'Время', 'Код врача', 'Код пациента', 'Описание']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Record.objects.all().values_list('date',  'rec_time', 'doctors_name', 'patient_id', 'description',)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response