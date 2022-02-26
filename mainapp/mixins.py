from django.views.generic.base import ContextMixin

from .models import Topic


class PopularTopicsMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pop_topics'] = Topic.get_top_topics()
        return context
