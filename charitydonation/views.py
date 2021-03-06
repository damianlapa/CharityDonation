from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from charitydonation.models import Category, Donation, Institution, UserToken
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import check_password, make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import random
from django.core.mail import send_mail
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import datetime


def create_token(token_length):
    signs = (
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n',
        'm', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A',
        'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M')
    token = ''
    for _ in range(0, token_length):
        token += str(signs[random.randint(0, len(signs) - 1)])

    return token


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

        paginator = Paginator(institutions, 5)

        page = int(request.GET.get("page", 1))

        institutions_all = paginator.get_page(page)


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

            new_user = User.objects.create_user(username=email, email=email, password=password, first_name=name,
                                                last_name=surname,
                                                is_active=False)
            user_token = create_token(16)
            UserToken.objects.create(user=new_user, token=user_token)

            html = """\
            <html>
              <body>
                <p>Hi,<br>
                   Congratulations for create new account! Enter this link to activate your account: <br>
                   <a href="{}/{}">Activate Your Account</a>
                </p>
              </body>
            </html>
            """.format(os.environ.get('ACTIVATE_LINK'), user_token)

            send_mail('New Account', '', 'Charity Donation', (email,), html_message=html)

            return redirect('landing-page')


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
        submit_value = request.POST.get('submit')

        if submit_value == 'Edytuj':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')

            user = request.user

            user.first_name = first_name
            user.last_name = last_name
            user.email = email

            user.save()

            return redirect('edit')

        else:
            old_password = request.POST.get('old_pass')
            new_password = request.POST.get('new_pass')
            repeated_new_pass = request.POST.get('new_pass_repeat')

            if new_password == repeated_new_pass:
                if check_password(old_password, request.user.password):
                    user = request.user
                    user.password = make_password(new_password)
                    user.save()
                    return redirect('landing-page')
            else:
                statement = "Passwords aren't this same"
                return render(request, 'statement.html', locals())


class CorrectPassword(View):

    def post(self, request):
        password = request.POST.get('password')
        if check_password(password, request.user.password):
            print('ok')
            return HttpResponse(json.dumps('correct-password'))
        else:
            return HttpResponse(json.dumps('incorrect'))


class ValidateAccount(View):

    def get(self, request, token_value):
        user_token = UserToken.objects.get(token=token_value)

        user = user_token.user

        if user.is_active:

            statement = 'User was already activated!'

            return render(request, 'statement.html', locals())

        else:

            difference = datetime.datetime.now(datetime.timezone.utc) - user_token.date_created

            if difference > datetime.timedelta(hours=1):

                user_token.delete()
                new_token = create_token(16)
                UserToken.objects.create(user=user, token=new_token)

                html = """\
                            <html>
                              <body>
                                <p>Hi,<br>
                                   We've created for you new token! Enter this link to activate your account: <br>
                                   <a href="{}/{}">Activate Your Account</a>
                                </p>
                              </body>
                            </html>
                            """.format(os.environ.get('ACTIVATE_LINK'), new_token)

                send_mail('Activate Account', '', 'Charity Donation', (user.email,), html_message=html)

                statement = 'Token out of date. We have send you new token to activate your account'

                return render(request, 'statement.html', locals())

            else:

                user_to_activate = user_token.user
                user_to_activate.is_active = True
                user_to_activate.save()
                login(request, user_to_activate)
                return redirect('landing-page')


class ForgotPassword(View):

    def get(self, request):
        return render(request, 'pass-forgot.html')

    def post(self, request):
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            reset_token = create_token(16)
            old_token = UserToken.objects.get(user=user).delete()
            UserToken.objects.create(user=user, token=reset_token, password_reset=True)

            html = """\
                        <html>
                          <body>
                            <p>Hi,<br>
                               Link to change your password: <br>
                               <a href="{}/{}">Change Your Account</a>
                            </p>
                          </body>
                        </html>
                        """.format(os.environ.get('RESET_LINK'), reset_token)

            send_mail('Reset Password', '', 'Charity Donation', (user.email,), html_message=html)

            statement = 'Na adres email: {} został wysłany link do zmiany hasła.'.format(user.email)
            return render(request, 'statement.html', {'statement': statement})
        except Exception as e:
            statement = 'Nie ma takiego użytkownika w bazie danych'
            return render(request, 'statement.html', {'statement': statement})


class ResetPassword(View):

    def get(self, request, reset_token):
        user_token = get_object_or_404(UserToken, token=reset_token)
        if user_token.password_reset:
            return render(request, 'pass-reset.html')

    def post(self, request, reset_token):
        user_token = get_object_or_404(UserToken, token=reset_token)
        user = user_token.user

        new_password = request.POST.get('pass')
        repeated_pass = request.POST.get('pass2')

        if new_password == repeated_pass:
            user.password = make_password(new_password)
            user.save()
            statement = 'Ustawiono nowe hasło'
            user_token.delete()
            return render(request, 'statement.html', locals())

        else:
            statement = 'Hasła nie są takie same'
            return render(request, 'statement.html', locals())