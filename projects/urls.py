from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('projects/', views.projects, name='projects-list'),
    path('projects/tasks/', views.tasks, name='projects-tasks'),
    path('projects/tasks/<int:project_id>/', views.project_tasks, name='projects-tasks-project'),
]