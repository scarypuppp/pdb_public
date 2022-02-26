from PIL import Image

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from users.models import User, PDBUser, IPClient


def get_problem_url(obj, view_name):
    return reverse(view_name, kwargs={'slug': obj.slug})


class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass


class Branch(models.Model):

    name = models.CharField(max_length=255, verbose_name="Наименование раздела")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Topic(models.Model):

    branch = models.ForeignKey(Branch, default='', verbose_name="Раздел", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="Наименование темы")
    slug = models.SlugField(unique=True)

    def views_count(self):
        ans = sum([i.views_count() for i in self.related_problems.all()])
        return ans

    def get_top_topics(self):
        qs = Topic.objects.all()
        topics = sorted(qs, key=lambda x: x.views_count())
        topics.reverse()
        return topics[:5]

    def __str__(self):
        return '{}'.format(self.name)


class Problem(models.Model):

    MIN_RESOLUTION = (100, 100)
    MAX_RESOLUTION = (1000, 1000)
    MAX_IMAGE_SIZE = 3145728

    ANSWER_CHOICES = (
        ('ED', 'Один'),
        ('MP', 'Несколько'),
        ('NM', 'Число'),
        ('EX', 'Развернутый')
    )

    branch = models.ForeignKey(Branch, null=True, verbose_name="Раздел", on_delete=models.CASCADE, related_name='branch_related_problems')
    topic = models.ForeignKey(Topic, verbose_name="Тема", on_delete=models.CASCADE, related_name="related_problems")
    source = models.CharField(default='', max_length=255, verbose_name="Источник")
    description = models.TextField(verbose_name='Описание задачи')
    answer_type = models.CharField(max_length=255, verbose_name="Тип ответа", choices=ANSWER_CHOICES, default='EX')
    with_image = models.BooleanField(default=False, verbose_name='Задача с картинкой')

    # Optional fields

    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    answer = models.CharField(null=True, blank=True, max_length=32, verbose_name="Числовой ответ")

    author = models.ForeignKey(User, default=1,  on_delete=models.CASCADE)
    viewed_ips = models.ManyToManyField(IPClient, blank=True, null=True, verbose_name="viewed ips")
    answer_choices = models.JSONField(verbose_name="Варианты ответа", null=True, blank=True, default=dict)

    def __str__(self):
        return self.source

    def get_absolute_url(self):
        return get_problem_url(self, 'problem_detail')

    def featured_count(self):
        return self.related_featured.count()

    def views_count(self):
        return self.viewed_ips.all().count()

    def save(self, *args, **kwargs):
        if self.with_image:
            image = self.image
            img = Image.open(image)
            min_height, min_width = self.MIN_RESOLUTION
            max_height, max_width = self.MAX_RESOLUTION
            if img.height < min_height or img.width < min_width:
                raise MinResolutionErrorException('Разрешение изображения меньше минимального')
            if img.height > max_height or img.width > max_width:
                raise MaxResolutionErrorException('Разрешение изображения больше максимального')
        else:
            self.image = None

        self.branch = Topic.objects.get(name__contains=self.topic.name).branch
        return super().save(*args, **kwargs)


class Collection(models.Model):

    name = models.CharField(max_length=255, verbose_name="Название коллекции")
    solve_time = models.DurationField()
    problems = models.ManyToManyField(Problem, verbose_name="Задачи")

    def __str__(self):
        return '{}'.format(self.name)


class FeaturedProblems(models.Model):

    owner = models.ForeignKey(PDBUser, verbose_name='Владелец', on_delete=models.CASCADE, related_name="featured_problems")
    problems = models.ManyToManyField(Problem, blank=True, null=True, related_name="related_featured")

    def __str__(self):
        return 'Избранное для пользователя {}'.format(self.owner.user.username)
