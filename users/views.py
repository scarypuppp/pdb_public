from django.contrib import messages
from django.shortcuts import render, redirect
import requests
from django.contrib.auth import logout, authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from .models import User
from .forms import LoginForm, RegistrationForm, ResetPasswordForm, ResetPasswordSendForm
from django.template.loader import render_to_string
from .models import PDBUser
from django.utils.encoding import force_bytes, force_str, force_text
from .utils import generate_activation_token, generate_forgot_token
from django.core.mail import EmailMessage
import threading
from mainapp.models import FeaturedProblems, Problem

from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'PDB - Подтверждение адреса электронной почты'
    email_body = render_to_string('users/activation_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_activation_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body, from_email='pdb-reply@mail.ru', to=[user.email])
    EmailThread(email).start()


def send_password_reset_email(user, request):

    current_site = get_current_site(request)
    email_subject = 'PDB - Сброс пароля'
    email_body = render_to_string('users/password_reset_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_forgot_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body, from_email='pdb-reply@mail.ru', to=[user.email])
    EmailThread(email).start()


class LoginView(View):

    def get(self, request, *args, **kwargs):

        context = dict()

        if not request.user.is_authenticated:
            form = LoginForm(request.POST or None)
            context['form'] = form
            return render(request, 'users/login_form.html', context)
        else:
            return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):

        form = LoginForm(request.POST or None)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if not form.cleaned_data.get('remember_me'):
                self.request.session.set_expiry(0)
            user = authenticate(username=username, password=password)
            try:
                # obj = PDBUser.objects.get(user_id=user.pk)
                if not user.pdbuser.email_verified:
                    messages.warning(request, 'Адрес электронной почты не подтвержден. Пожалуйста, проверьте вашу электронную почту')
                    return redirect('login-view')
            except PDBUser.DoesNotExist:
                PDBUser(user=user, patronymic='', email_verified=True, editor=True).save()
                FeaturedProblems.objects.create(
                    owner=user.pdbuser,
                )
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                messages.error(request, 'Ошибка авторизации')
        return render(request, 'users/login_form.html', {'form': form})


class RegistrationView(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = RegistrationForm(request.POST or None)
            context = {'form': form}
            return render(request, 'users/registration.html', context)
        else:
            return redirect('main_page')

    def post(self, request, *args, **kwargs):

        form = RegistrationForm(request.POST or None)
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if not result['success']:
            messages.error(request, 'Капча просрочена или не отмечена. Пожалуйста, повторите попытку')

        if form.is_valid() and result['success']:
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            new_pdbuser = PDBUser.objects.create(
                user=new_user,
                patronymic=form.cleaned_data['patronymic'],
                email_verified=False
            )
            FeaturedProblems.objects.create(
                owner=new_pdbuser,
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            messages.info(request, 'Мы отправили на ваш Email сообщение с подтверждением регистрации')
            # messages.success(request, 'Вы успешно создали аккаунт')
            # login(request, user)
            send_activation_email(user, request)
            return redirect('login-view')
        context = {'form': form}
        return render(request, 'users/registration.html', context)


class ResetPasswordEmailSend(View):

    def get(self, request, *args, **kwargs):

        form = ResetPasswordSendForm(request.POST or None)
        return render(request, 'users/password_reset_send.html', {'form': form})

    def post(self, request, *args, **kwargs):

        form = ResetPasswordSendForm(request.POST or None)

        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email)
            if user.exists():
                send_password_reset_email(user.get(email=email), request)
                messages.info(request, 'Сообщение с данными для сброса пароля отправлено на почту')
                return redirect('login-view')
            messages.error("Пользователь с данной почтой не найден")

        return render(request, 'users/password_reset_send.html', {'form': form})


class ResetPasswordEmail(View):

    def get(self, request, uidb64, token):

        form = ResetPasswordForm()

        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if user and generate_forgot_token.check_token(user, token):
            return render(self.request, 'users/password_reset.html', {'form': form})
        else:
            messages.error(self.request, 'Ссылка более не действительна')
            return redirect('login-view')

    def post(self, request, uidb64, token):

        form = ResetPasswordForm(self.request.POST)

        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if user and generate_forgot_token.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                new_password_confirm = form.cleaned_data['new_password_confirm']

                if new_password == new_password_confirm:
                    user.set_password(new_password)
                    user.save()
                    messages.success(self.request, 'Пароль успешно изменен')
                    return redirect('login-view')
            else:
                return render(self.request, 'users/password_reset.html', {'form': form})
        messages.error(self.request, 'Произошла неизвестная ошибка. Пожалуйста, повторите попытку')
        return redirect('login-view')


class ActivateUser(View):

    def get(self, request, uidb64, token):

        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if user and generate_activation_token.check_token(user, token):
            user.pdbuser.email_verified = True
            user.pdbuser.save()
            messages.success(self.request, 'Адрес электронной почты успешно подтвержден')
            return redirect('login-view')

        return render(self.request, 'users/activate-failed.html', {'user': user})


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('main_page')