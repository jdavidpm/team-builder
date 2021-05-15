from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('projects/', views.projects_list, name='projects-list'),
    path('projects/create', views.projects_create, name='projects-create'),
    path('projects/<int:id>/', views.project_item, name='projects-item'),
    path('projects/<int:id>/update/', views.project_update, name='projects-update'),
    path('tasks/', views.tasks, name='projects-tasks'),
    path('tasks/<str:filter_by>/<int:object_id>/', views.filtered_tasks, name='projects-filteredtasks'),
    path('tasks/new/<int:project_id>', views.createTask, name='projects-create_task'),
    path('tasks/<int:pk>/', views.updateTask, name='projects-update_task'),
    path('tasks/<int:pk>/delete/', views.deleteTask, name='projects-delete_task'),
]