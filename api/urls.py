from django.urls import path,include

urlpatterns = [
    path('account/',include('ACCOUNTS.urls')),
    path('home/',include('TASK.urls')),
    
]