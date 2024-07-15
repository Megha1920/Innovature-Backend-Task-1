from django.urls import path
from .views import TaskView

urlpatterns = [
    path('todo/', TaskView.as_view(), name='task-list-create'),
    path('todo/<uuid:uid>/', TaskView.as_view(), name='task-detail'),
]
