from django import template
from django.utils.safestring import mark_safe
from random import shuffle
from mainapp.models import Topic

register = template.Library()

ANSWER_CONTAINER = """
    <div class = "problem_answer_container">{}</div>
"""
CHOICES_CONTENT = """
    <div class = "problem_choices">{}</div>
"""

NUM_ANSWER_CONTENT = """
    <div class = "problem_num_answer">
        <input type="text" class = "form-control form-control-sm" name="{}" placeholder="Введите ответ">
    </div>
"""

POP_CAT_CONTAINER = '<div class ="tb-row tb-row-content" >{}</div>'
POP_CAT_ITEM = '<span class ="pop-cat-name">{}</span><span class ="pop-cat-views">{}</span>'

@register.filter
def pop_cats():
    cats = Topic.objects.all()
    pop_cat_content = ''
    print(cats)
    for cat in cats:
        name = cat.name
        views = sum([i.views_count() for i in cat.problem_set])
        print(views)
        pop_cat_content += POP_CAT_ITEM.format(name, views)

    return mark_safe(POP_CAT_CONTAINER.format(pop_cat_content))

@register.filter
def get_value(choice):
    print(type(choice), choice)
    return ''
