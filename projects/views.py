from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def projects(request):
    projects_list = request.user.created_projects.all()
    return render(request, 'projects/projects.html', {'title': 'Proyectos', 'projects_list': projects_list})

def tasks(request):
    tasks_list = request.user.assigned_tasks.all()
    context = {
        'tasks': tasks_list,
        'title': 'Tareas'
    }
    return render(request, 'projects/tasks.html', context)