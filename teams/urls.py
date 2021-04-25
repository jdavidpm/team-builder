from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('teams/', views.teams, name='teams-list'),
]