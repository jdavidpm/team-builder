from django.urls import path
from django.contrib.auth import views as authViews
from . import views

urlpatterns = [
    path('profile/', views.profile, name='users-profile'),
    path('signup/', views.signup, name='users-signup'),
    path('signin/', authViews.LoginView.as_view(template_name='users/signin.html'), name='users-signin'),
    path('signout/', authViews.LogoutView.as_view(template_name='users/signout.html'), name='users-signout')
]