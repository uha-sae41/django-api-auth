from django.urls import path

from . import views

urlpatterns = [
    path('api/', views.UserView.as_view()),
    path('api/register/', views.UserRegistrationView.as_view()),
    path('api/login/', views.UserLoginView.as_view()),
    path('api/user/', views.UserDetailView.as_view()),
    path('api/user/<int:id>/', views.UserDetailByIdView.as_view()),
    path('api/validate-token/', views.ValidateTokenView.as_view()),
    path('api/change-password/', views.ChangePasswordView.as_view()),
    path('api/delete-account/', views.DeleteAccountView.as_view()),
    path('api/edit-account/', views.UserUpdateView.as_view()),
    path('api/edit-account/<int:id>/', views.UserUpdateViewByIdView.as_view()),
]