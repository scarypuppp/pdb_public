from PIL import Image

from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import *
from django import forms
from .forms import ProblemForm
from users.models import PDBUser, IPClient


class ProblemAdminForm(ProblemForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            '<span style="color:red; font-size: 14px">Загружайте изображения с минимальным разрешением {}x{}</span>'.format(
                *Problem.MIN_RESOLUTION
            )
        )

    def clean_image(self):
        if self.cleaned_data['with_image']:
            image = self.cleaned_data['image']
            img = Image.open(image)
            min_height, min_width = Problem.MIN_RESOLUTION
            max_height, max_width = Problem.MAX_RESOLUTION
            if image.size > Problem.MAX_IMAGE_SIZE:
                raise ValidationError('Размер изображения не доллжен превышать 3МБ')
            if img.height < min_height or img.width < min_width:
                raise ValidationError('Разрешение изображения меньше минимального')
            if img.height > max_height or img.width > max_width:
                raise ValidationError('Разрешение изображения больше максимального')
            return image

class ProblemSubtopicChoiceField(forms.ModelChoiceField):
    pass


class ProblemAdmin(admin.ModelAdmin):

    change_form_template = 'admin.html'
    exclude = ['branch']
    form = ProblemAdminForm


admin.site.register(Topic)
admin.site.register(Branch)
admin.site.register(IPClient)

admin.site.register(Collection)
admin.site.register(PDBUser)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(FeaturedProblems)
