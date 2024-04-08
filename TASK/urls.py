from django.urls import path
from TASK.views import TaskView

urlpatterns = [
    path('todo/',TaskView.as_view()),
     
]