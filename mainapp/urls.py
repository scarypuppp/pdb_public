from django.urls import path
from .views import *


urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('problems/<str:branch>/', ProblemList.as_view(), name='problem-list'),
    path('problems/<str:branch>/<str:topic>', ProblemList.as_view(), name='problem-list'),
    path('problem/detail/<int:pk>/', ProblemDetailView.as_view(), name='problem_detail'),
    path('create-problem/', AddProblem.as_view(), name='add-problem'),
    path('update-problem/<int:pk>', UpdateProblem.as_view(), name='update-problem'),
    path('profile/my-problems', UserProfileMyProblems.as_view(), name='user-my-problems'),
    path('profile/featured', UserProfileFeatured.as_view(), name='user-featured'),
    path('categories/', Categories.as_view(), name='cats-list')
]