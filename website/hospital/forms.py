from django.forms import ModelForm
from .models import Doctor, Record, CustomUser
from  django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class PatientForm(UserCreationForm):
    username = forms.CharField(label='', max_length=30, min_length=5, required=True, widget=forms.TextInput(attrs={'placeholder':'Имя пользователя'}))
    email = forms.EmailField(label='', min_length=5, max_length=40, required=True, widget=forms.TextInput(attrs={'placeholder':'Электронная почта'}))
    password1 = forms.CharField(label='', max_length=40, min_length=10, required=True, widget=forms.PasswordInput(attrs={'placeholder':'Пароль'}))
    password2 = forms.CharField(label='', max_length=40, min_length=10, required=True, widget=forms.PasswordInput(attrs={'placeholder':'Повторите пароль'}))
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    email = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'placeholder':'Электронная почта'}))
    password = forms.CharField(label='', required=False, widget=forms.PasswordInput(attrs={'placeholder':'Пароль'}))
    class Meta:
        model = User
        fields = ['email', 'password']

class RecordForm(forms.ModelForm):
    date = forms.DateField(label='Дата',widget=forms.DateInput(attrs={'type':'date'}))
    rec_time = forms.DateTimeField(label='Время',widget=forms.DateInput(attrs={'type':'time'}))
    doctors_name = forms.ModelChoiceField(label='ФИО врача',queryset=Doctor.objects.all())
    description = forms.CharField(label='Описание',max_length=50, required=False)
    class Meta:
        model = Record
        fields = ['date', 'rec_time', 'doctors_name', 'description']


class MyDataEditForm(forms.ModelForm):
    username = forms.CharField(label='', max_length=30, min_length=5, required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'}))
    email = forms.EmailField(label='', min_length=5, max_length=40, required=False,
                             widget=forms.TextInput(attrs={'placeholder': 'Электронная почта'}))
    first_name = forms.CharField(label='', max_length=20, min_length=2, required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    second_name = forms.CharField(label='', max_length=20, min_length=2, required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}))
    last_name = forms.CharField(label='', max_length=20, min_length=2, required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'Отчество'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'second_name', 'last_name']