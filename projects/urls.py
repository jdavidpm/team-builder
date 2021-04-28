from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('projects/', views.projects, name='projects-list'),
    path('projects/tasks/', views.schedule, name='schedule'),
    path('projects/tasks/<str:project>/', views.project_filtered_schedule, name='p-filtered-schedule'),
]