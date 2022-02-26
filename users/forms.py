from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Field, HTML
from django import forms
from .models import User


class RegistrationForm(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    patronymic = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='row'
            ),
            'email',
            'username',
            Div(
                Column('password', css_class='form-group col-md-6 mb-0'),
                Column('confirm_password', css_class='form-group col-md-6 mb-0'),
                css_class='row'
            ),
            HTML(
            """
            <script src='https://www.google.com/recaptcha/api.js'></script>
            <div class="g-recaptcha" data-sitekey="6LfEBmYdAAAAAE4p-M1-3hTnaCRrcCpzrBBD7cwn"></div>
            """
            ),
            HTML("""
            <input type="submit" name="submit" value="Создать аккаунт" class="trc-btn trc-btn-fluid trc-btn-dark" id="submit-id-submit">
            """),
        )

        self.fields['username'].widget.attrs.update({
            'autocomplete': 'off'
        })

        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Повтор пароля'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['first_name'].label = 'Имя'
        self.fields['patronymic'].label = 'Отчество'
        self.fields['email'].label = 'Электронная почта'

        self.fields['username'].help_text = ''

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким Email уже существует')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")
        if len(password) < 8:
            raise forms.ValidationError('Слишком короткий пароль')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password',
                  'email', 'last_name', 'first_name', 'patronymic']


class LoginForm(forms.ModelForm):
    # username = forms.CharField(max_length=100, label='Логин')
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}), label='Пароль')
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('username', css_class="login_form_input"),
            Field('password', css_class="login_form_input"),
            Div(
                Field('remember_me'),
                HTML("""<a href = "/users/forgot/" style = "margin-top:10px">Забыли пароль?</a>"""),
                css_class="login_form_footer"
            ),
            HTML("""
            <input type="submit" name="submit" value="Войти" class="trc-btn trc-btn-fluid trc-btn-dark login_form_submit" id="submit-id-submit">
            """),
        )
        self.fields['username'].label = ''
        self.fields['password'].label = ''
        self.fields['remember_me'].label = 'Запомнить меня'
        self.fields['username'].help_text = ''

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username)
        if not user.exists() or not user.first().check_password(password):
            raise forms.ValidationError("Неверное имя пользователя или пароль")
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class ResetPasswordSendForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('email'),
            HTML("""
            <input type="submit" name="submit" value="Отправить" class="trc-btn trc-btn-fluid trc-btn-dark login_form_submit" id="submit-id-submit">
            """),
        )
        self.fields['email'].label = ''

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким Email в системе не зарегистрирован")
        return email

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['email']


class ResetPasswordForm(forms.Form):

    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password_confirm = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('new_password'),
            Field('new_password_confirm'),
            HTML("""
            <input type="submit" name="submit" value="Сбросить пароль" class="trc-btn trc-btn-fluid trc-btn-dark login_form_submit" id="submit-id-submit">
            """),
        )
        self.fields['new_password'].label = 'Новый пароль'
        self.fields['new_password_confirm'].label = 'Подтверждение пароля'

    def clean(self):
        new_password = self.cleaned_data['new_password']
        new_password_confirm = self.cleaned_data['new_password_confirm']
        if new_password != new_password_confirm:
            raise forms.ValidationError("Пароли не совпадают")
        if len(new_password) < 8:
            raise forms.ValidationError('Слишком короткий пароль')
        return self.cleaned_data
