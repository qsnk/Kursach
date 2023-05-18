from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, help_text='', verbose_name='Имя пользователя', unique=True)
    email = models.CharField(max_length=40, help_text='Введите вашу электронную почту',
                                 verbose_name='Электронная почта', unique=True, )
    password = models.CharField(max_length=30, help_text='Введите пароль', verbose_name='Пароль')
    first_name = models.CharField(max_length=20, help_text='Введите ваше имя', verbose_name='Имя', null=True)
    second_name = models.CharField(max_length=20, help_text='Введите вашу фамилию', verbose_name='Фамилия', null=True)
    last_name = models.CharField(max_length=25, help_text='Введите ваше отчество', verbose_name='Отчество', null=True)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f'{self.email}'

class Speciality(models.Model):
    name = models.CharField(max_length=30, help_text='Введите специальность', verbose_name='Специальность')

    def __str__(self):
        return self.name

class Doctor(models.Model):
    first_name = models.CharField(max_length=20, help_text='Введите ваше имя', verbose_name='Имя')
    second_name = models.CharField(max_length=20, help_text='Введите вашу фамилию', verbose_name='Фамилия')
    last_name = models.CharField(max_length=25, help_text='Введите ваше отчество', verbose_name='Отчество')
    gender = models.BooleanField(help_text='Выберите ваш пол', verbose_name='Пол')  # forms.BooleanField
    birth_date = models.DateField(help_text='Введите дату рождения', verbose_name='Дата рождения')
    speciality = models.ForeignKey('Speciality', on_delete=models.CASCADE, help_text='Выберите специальность', verbose_name='Специальность', null=True)
    email = models.CharField(max_length=40, help_text='Введите вашу электронную почту', verbose_name='Электронная почта')  # forms.emailField
    username = models.CharField(max_length=20, help_text='', verbose_name='Имя пользователя')
    password = models.CharField(max_length=30, help_text='Введите пароль', verbose_name='Пароль')
    address = models.CharField(max_length=40, help_text='Введите адрес', verbose_name='Адрес', null=True)
    phone = models.CharField(max_length=12, help_text='Введите телефон', verbose_name='Телефон', null=True)

    def __str__(self):
        return f'{self.second_name} {self.first_name} {self.last_name}'

class Record(models.Model):
    date = models.DateField(help_text='Выберите дату записи', verbose_name='Дата записи')
    rec_time = models.TimeField(help_text='Выберите время записи', verbose_name='Время записи')
    doctors_name = models.ForeignKey(Doctor, help_text='Введите инициалы доктора', verbose_name='Инициалы доктора', on_delete=models.CASCADE)
    patient = models.ForeignKey(CustomUser, help_text='Введите ФИО', verbose_name='Пациент', on_delete=models.CASCADE)
    description = models.CharField(max_length=100, help_text='Опишите проблему', verbose_name='Описание', null=True)

    def __str__(self):
        return f'{self.date} {self.rec_time} к {self.doctors_name}'

    @classmethod
    def create(cls, date, time, doc_name, patient, description):
        return cls(date = date, rec_time=time, doctors_name=doc_name, patient=patient, description=description)
