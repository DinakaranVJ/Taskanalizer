from django.urls import path
from .views import AnalyzeTasksView, SuggestTasksView, frontend

urlpatterns = [
    path("", frontend, name="frontend"),
     path('analyze/', AnalyzeTasksView.as_view(), name='analyze'),
    path('suggest/', SuggestTasksView.as_view(), name='suggest'),
]
