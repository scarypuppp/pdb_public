from django.urls import path
from .views import *


urlpatterns = [
    path('sign-in/', LoginView.as_view(), name='login-view'),
    path('sign-up/', RegistrationView.as_view(), name='registration-view'),
    path('activate/<uidb64>/<token>', ActivateUser.as_view(), name='activate-view'),
    path('forgot/', ResetPasswordEmailSend.as_view(), name='forgot-password-send'),
    path('forgot/<uidb64>/<token>', ResetPasswordEmail.as_view(), name='forgot-password'),
    path('logout/', LogoutView.as_view(), name='logout_page'),
]