from django.urls import path

from . import views

urlpatterns = [
    path('signin/', views.signin, name='users-signin'),
    path('signup/', views.signup, name='users-signup')
]