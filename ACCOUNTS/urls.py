from django.urls import path
from ACCOUNTS.views import Registerview,Loginview,TokenRefreshView

urlpatterns = [
    path('register/',Registerview.as_view()),
     path('login/',Loginview.as_view()),
     path('refresh/', TokenRefreshView.as_view()),
]