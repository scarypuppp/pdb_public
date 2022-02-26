from ajax_select.fields import AutoCompleteSelectField
from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Field, HTML
from django import forms
from .models import Problem, User, Topic


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = '__all__'


class ProblemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['answer_choices'].widget = forms.HiddenInput()
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('branch'),
                    Field('topic'),
                    css_class="col-lg-6"
                ),
                Column(
                    Field('source'),
                    Field('with_image'),
                    Field('image'),
                    InlineRadios('answer_type'),
                    css_class="col-lg-6"
                ),
                Column(
                    Field('description'),
                    Div(
                        HTML(
                        """
                            <span>Варианты ответа:</span>
                            <div class=' trc-circle-icon answer-choice-add' id='ans_add'><i class="bi bi-plus-lg"></i></div>
                            <div class=' trc-circle-icon answer-choice-remove' id='ans_remove'><i class="bi bi-dash-lg"></i></div>
                        """),
                        Div(css_class='answer_choice_container', id='ans_container'),
                        css_class='answer_choice_custom form-group',
                    ),
                    Field('answer', css_class="form-control-sm"),
                    'answer_choices',
                    css_class="col-lg-12"
                ),
                css_class="row"
            ),
            HTML("""
            <input type="submit" name="submit" value="Сохранить" class="trc-btn trc-btn-dark form-group" id="submit-id-submit">
            """)
        )

    def clean_answer(self):
        answer = self.cleaned_data['answer']
        answer_type = self.cleaned_data['answer_type']
        if answer_type == 'NM':
            if answer is None:
                raise forms.ValidationError("Введите числовой ответ")
        else:
            if answer is not None:
                answer = None
        return answer

    def clean_image(self):
        with_image = self.cleaned_data['with_image']
        image = self.cleaned_data['image']
        if with_image:
            if image is None:
                raise forms.ValidationError("Выберите изображение")
        return image

    def clean(self):
        answer_choices = self.cleaned_data['answer_choices']
        answer_type = self.cleaned_data['answer_type']
        if answer_type == 'ED' or answer_type == 'MP':
            if len(answer_choices['choices']) not in range(2, 6):
                raise forms.ValidationError("Выберите от 2 до 5 вариантов ответа")
            if len(answer_choices['correct']) == 0:
                raise forms.ValidationError("Выберите хотя бы один верный ответ")
            if any([i == '' for i in answer_choices['choices'].values()]):
                raise forms.ValidationError("Вариант ответа не должен быть пустым")
            if answer_type == 'ED':
                if len(answer_choices['correct']) > 1:
                    raise forms.ValidationError("Выбрано более 1 верных ответов")
        else:
            if answer_choices != {}:
                self.cleaned_data['answer_choices'] = {}

        return self.cleaned_data

    class Meta:
        model = Problem
        fields = ('branch', 'topic', 'with_image', 'image', 'description', 'source', 'answer_type', 'answer_choices', 'answer')
