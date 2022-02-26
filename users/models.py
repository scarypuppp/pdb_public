from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class PDBUser(models.Model):

    ANSWER_CHOICES = (
        ('ED', 'Один'),
        ('MP', 'Несколько'),
        ('NM', 'Число'),
        ('EX', 'Развернутый')
    )

    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    patronymic = models.CharField(max_length=255, verbose_name='Отчество')
    editor = models.BooleanField(verbose_name="Редактор", default=False, blank=True, null=True)
    avatar = models.ImageField(null=True, blank=True, verbose_name='Аватар')
    email_verified = models.BooleanField(default=False, verbose_name='Подтверждение email')

    def get_featured_problems(self):
        return self.featured_problems.first().problems.all()

    def __str__(self):
        return "Пользователь: {} {}".format(self.user.first_name, self.user.last_name)


class IPClient(models.Model):

    ip_address = models.CharField(verbose_name='IP', max_length=50)

    def __str__(self):
        return "IP: {}".format(self.ip_address)
