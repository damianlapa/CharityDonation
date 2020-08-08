"""PortfolioLab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from charitydonation.views import LandingPage, Login, Register, AddDonation, Logout, FormConfirmation, Profile, Take, \
    ProfileEdit, CorrectPassword, ValidateAccount

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', LandingPage.as_view(), name='landing-page'),
    path('login', Login.as_view(), name='login'),
    path('register', Register.as_view(), name='register'),
    path('add-donation', AddDonation.as_view(), name='add-donation'),
    path('logout', Logout.as_view(), name='logout'),
    path('form-confirmation', FormConfirmation.as_view(), name='form-confirmation'),
    path('profile', Profile.as_view(), name='profile'),
    path('take', Take.as_view(), name='take'),
    path('edit', ProfileEdit.as_view(), name='edit'),
    path('password-confirmation', CorrectPassword.as_view(), name='password-confirmation'),
    path('validate-account/<slug:token_value>', ValidateAccount.as_view(), name='validate-account')

]
