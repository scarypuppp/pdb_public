from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class TokenGeneratorActivation(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.pdbuser.email_verified)


class TokenGeneratorGorgot(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.password)


generate_activation_token = TokenGeneratorActivation()
generate_forgot_token = TokenGeneratorGorgot()
