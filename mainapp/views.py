from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, View
from .models import Problem, Branch, Topic
from .forms import ProblemForm
from users.models import IPClient
from .mixins import PopularTopicsMixin


class MainPageView(View):

    def sort_new(self, request, *args, **kwargs):
        qs = Problem.objects.all()
        problems = sorted(qs, key=lambda x: x.pk)
        problems.reverse()
        return problems[:10]

    def sort_views(self, request, *args, **kwargs):
        qs = Problem.objects.all()
        problems = sorted(qs, key=lambda x: x.views_count())
        problems.reverse()
        return problems[:10]

    def sort_pop(self, request, *args, **kwargs):
        qs = Problem.objects.all()
        problems = sorted(qs, key=lambda x: x.featured_count())
        problems.reverse()
        return problems[:10]

    def get(self, request, *args, **kwargs):
        context = dict()
        context['pop_topics'] = Topic.get_top_topics(self)
        sorting = ['popular', 'views', 'new']
        # context['pop_topics'] = Topic.get_top_topics(self)
        if 'sort-by' in request.GET:
            sort = request.GET['sort-by']
            if sort in sorting:
                if sort == 'new':
                    context['problems'] = self.sort_new(request)
                if sort == 'views':
                    context['problems'] = self.sort_views(request)
                if sort == 'popular':
                    context['problems'] = self.sort_pop(request)
            else:
                context['problems'] = self.sort_pop(request)
        else:
            context['problems'] = self.sort_pop(request)
        return render(request, 'mainapp/main_page.html', context)


class Categories(ListView):

    template_name = 'categories.html'
    model = Branch

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = context['object_list'].annotate(number_of_problems=Count('branch_related_problems'))
        context['pop_topics'] = Topic.get_top_topics(self)
        return context


class AddProblem(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.pdbuser.editor:
            form = ProblemForm
            return render(request, 'problem_form.html', {'form': form})
        else:
            messages.error(request, 'Вы не являетесь редактором')
            return HttpResponseRedirect('/profile/featured')

    def post(self, request, *args, **kwargs):
        if request.user.pdbuser.editor:
            form = ProblemForm(request.POST, request.FILES)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.author = request.user
                form.save()
                return redirect('/create-problem')
            else:
                messages.error(request, "Ошибка при добавлении задачи")
                return render(request, 'problem_form.html', {'form': form})
        else:
            messages.error(request, 'Вы не являетесь редактором')
            return HttpResponseRedirect('/profile/featured')



class UpdateProblem(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        if request.user.pdbuser.editor:
            problem = Problem.objects.filter(id=pk)
            if problem.exists():
                problem = problem.get(id=pk)
                if problem in Problem.objects.filter(author=request.user).all():
                    form = ProblemForm(instance=problem)
                    return render(request, 'problem_form.html', {'form': form})
                messages.error(request, "Недостаточно прав для редактирования данной задачи")
                return HttpResponseRedirect('/profile/my-problems')
            messages.error(request, "Задачи не существует или она удалена :(")
            return HttpResponseRedirect('/profile/my-problems')
        else:
            messages.error(request, 'Вы не являетесь редактором')
            return HttpResponseRedirect('/profile/featured')

    def post(self, request, pk, *args, **kwargs):
        if request.user.pdbuser.editor:
            problem = Problem.objects.filter(id=pk)
            if problem.exists():
                problem = problem.get(id=pk)
                if problem in Problem.objects.filter(author=request.user).all():
                    form = ProblemForm(request.POST, request.FILES, instance=problem)
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'Задача успешно изменена')
                        return redirect('/profile/my-problems')
                    else:
                        messages.error(request, "Ошибка при изменении задачи")
                        return render(request, 'problem_form.html', {'form': form})
                messages.error(request, "Недостаточно прав для редактирования данной задачи")
                return HttpResponseRedirect('/profile/my-problems')
            messages.error(request, "Задачи не существует или она удалена :(")
            return HttpResponseRedirect('/profile/my-problems')
        else:
            messages.error(request, 'Вы не являетесь редактором')
            return HttpResponseRedirect('/profile/featured')


class UserProfileMyProblems(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        if request.user.pdbuser.editor or request.user.is_superuser:
            page_number = request.GET.get('page')
            if request.user.is_superuser:
                problems = Problem.objects.all().order_by('pk')
            else:
                problems = Problem.objects.filter(author=request.user).order_by('pk')
            paginator = Paginator(problems[::-1], 10)
            page_obj = paginator.get_page(page_number)
            return render(request, 'my-problems.html', {
                'page_obj': page_obj,
                'paginator': paginator
            })

        else:
            messages.error(request, 'Вы не являетесь редактором')
            return HttpResponseRedirect('/profile/featured')


class UserProfileFeatured(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        page_number = request.GET.get('page')
        problems = request.user.pdbuser.get_featured_problems().order_by('pk')
        paginator = Paginator(problems[::-1], 10)
        page_obj = paginator.get_page(page_number)
        return render(request, 'featured.html', {
            'page_obj': page_obj,
            'paginator': paginator
        })


class ProblemList(View):

    def get(self, request, *args, **kwargs):

        context = dict()

        problems = Problem.objects.all().order_by('pk')
        page_number = request.GET.get('page')
        dct = self.kwargs

        if 'branch' in dct.keys():
            problems = problems.filter(branch__slug=dct['branch'])
        if 'topic' in dct.keys():
            problems = problems.filter(topic__slug=dct['topic'])
        if problems.count() == 0:
            raise Http404

        paginator = Paginator(problems, 10)
        page_obj = paginator.get_page(page_number)

        return render(request, 'problem_list.html', {
            'page_obj': page_obj,
            'paginator': paginator,
            'pop_topics': Topic.get_top_topics(self)
        })


class ProblemDetailView(DetailView):

    def get_client_ip(self, request, *args, **kwargs):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    model = Problem
    queryset = model._base_manager.all()
    context_object_name = 'problem'
    template_name = 'problem_detail.html'
    slug_url_kwarg = 'slug'

    def get_object(self):
        obj = super().get_object()

        client, created = IPClient.objects.get_or_create(ip_address=self.get_client_ip(self.request))
        obj.viewed_ips.add(client)
        obj.save()

        return obj



