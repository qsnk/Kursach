"""
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hospital import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contacts/', views.contacts, name='contacts'),
    path('login/', views.sign_in, name='login'),
    path('login/personal_account/', views.personal_account, name='personal_account'),
    path('login/personal_account/delete/<int:id>/', views.delete, name='delete'),
    path('login/personal_account/record/', views.make_record, name='make_record'),
    path('login/personal_account/my_data/', views.get_data, name='account_data'),
    path('login/personal_account/edit/', views.edit_data, name='account_edit'),
    path('login/personal_account/export/', views.export_page, name='export'),
    path('login/personal_account/export/export_users_xls', views.export_users_xls, name='export_users'),
    path('login/personal_account/export/export_doctors_xls', views.export_doctors_xls, name='export_doctors'),
    path('login/personal_account/export/export_records_xls', views.export_records_xls, name='export_records'),
    path('about/', views.about, name='about'),
    path('signup/', views.sign_up, name='signup'),
    path('logot', views.log_out, name='logout'),
    path('FAQ/', views.faq, name='FAQ'),
    path('news/', views.news, name='news'),
    path('admin/', admin.site.urls),
]
