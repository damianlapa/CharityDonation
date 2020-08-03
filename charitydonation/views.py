from django.shortcuts import render, redirect
from django.views import View
from charitydonation.models import Category, Donation, Institution
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class LandingPage(View):

    def get(self, request):
        bags = Donation.objects.all()
        bags_quantity = 0
        for bag in bags:
            bags_quantity += bag.quantity
        institutions = Institution.objects.all()
        institutions_quantity = institutions.count()
        foundations = institutions.filter(type='Fundacja')
        organizations = institutions.filter(type='Organizacja pozarządowa')
        local_collections = institutions.filter(type='Zbiórka lokalna')
        return render(request, 'index.html', locals())


class AddDonation(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):

        username = request.user.username
        categories = Category.objects.all()

        return render(request, 'form.html', locals())


class Login(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)

        if user:
            login(request, user)
            return redirect('landing-page')

        else:
            return redirect('register')


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('login')


class Register(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            User.objects.create_user(username=email, email=email, password=password, first_name=name, last_name=surname)

            return redirect('login')