from django.shortcuts import render, redirect
from django.views import View
from charitydonation.models import Category, Donation, Institution
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import check_password
import json

class UserData(View):
    def get(self, request):
        if request.user.is_anonymous:
            username = 'Gość'
        else:
            if request.user.is_superuser:
                user_admin = True
            username = request.user.email


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

        if request.user.is_anonymous:
            username = 'Gość'
        else:
            if request.user.is_superuser:
                user_admin = True
            username = request.user.email

        return render(request, 'index.html', locals())


class AddDonation(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        username = request.user.username
        categories = Category.objects.all()
        organizations = Institution.objects.all()

        return render(request, 'form.html', locals())

    def post(self, request):
        quantity = request.POST.get('bags')
        categories = request.POST.getlist('categories')
        institution = Institution.objects.get(name=request.POST.get('organization'))
        address = request.POST.get('address')
        phone_number = request.POST.get('phone')
        city = request.POST.get('city')
        zip_code = request.POST.get('postcode')
        pick_up_date = request.POST.get('data')
        pick_up_time = request.POST.get('time')
        pick_up_comment = request.POST.get('more_info')
        user = User.objects.get(email=request.user.email)

        new_donation = Donation.objects.create(quantity=quantity, institution=institution, address=address,
                                               phone_number=phone_number, city=city, zip_code=zip_code,
                                               pick_up_date=pick_up_date, pick_up_time=pick_up_time,
                                               pick_up_comment=pick_up_comment, user=user)

        for category in categories:
            new_donation.categories.add(Category.objects.get(name=category))

        new_donation.save()

        return redirect('form-confirmation')


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


class FormConfirmation(View):

    def get(self, request):
        return render(request, 'form-confirmation.html')


class Profile(View):

    def get(self, request):
        if request.user.is_anonymous:
            username = 'Gość'
        else:
            if request.user.is_superuser:
                user_admin = True
            username = request.user.email
            user_first_name = request.user.first_name
            user_last_name = request.user.last_name
            user_email = request.user.email

            user_donations = Donation.objects.all().filter(user=User.objects.get(email__exact=user_email))
        return render(request, 'profile.html', locals())


class Take(View):

    def get(self, request):
        donation_id = request.GET.get('organization')
        donation = Donation.objects.get(id=donation_id)
        donation.is_taken = True
        donation.save()
        z = json.dumps(donation_id)
        return HttpResponse(z)


class ProfileEdit(View):

    def get(self, request):
        return render(request, 'edit-user-data.html', locals())

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        user = request.user

        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        user.save()

        return redirect('edit')


class CorrectPassword(View):

    def post(self, request):
        password = request.POST.get('password')
        print(password)
        print(check_password(password, request.user.password))
        if check_password(password, request.user.password):
            print('ok')
            return HttpResponse(json.dumps('correct-password'))
        else:
            return HttpResponse(json.dumps('incorrect'))

