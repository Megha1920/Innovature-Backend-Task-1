from django.urls import path,include

urlpatterns = [
    path('account/',include('ACCOUNTS.urls')),
    path('task/',include('TASK.urls')),
    path('file/',include('FILEHANDLE.urls')),
]