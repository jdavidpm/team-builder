from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('teams/', views.teams, name='teams-list'),
    path('teams/create/', views.team_create, name='teams-create'),
    path('teams/<int:id>/evaluate/', views.team_evaluate, name='teams-evaluate'),
    path('teams/<int:id>/', views.teams_item, name='teams-item'),
    path('teams/<int:id>/update/', views.team_update, name='team-update'),
    path('teams/<int:id>/update/members/', views.team_update_members, name='teams-update-members'),
]