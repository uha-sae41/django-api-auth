from django.urls import path

from . import views
from .views import AuthView

urlpatterns = [
    path('api/', AuthView.as_view()),
    path('api/register/', views.UserRegistrationView.as_view()),
    path('api/login/', views.UserLoginView.as_view()),
]