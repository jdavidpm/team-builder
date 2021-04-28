from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import Task


@login_required
def projects(request):
    projects_list = request.user.created_projects.all()
    return render(request, 'projects/projects.html', {'title': 'Proyectos', 'projects_list': projects_list})


@login_required
def schedule(request):
    return project_filtered_schedule(request)

@login_required
def project_filtered_schedule(request, project=""):
    if not project:
        tasks_list = request.user.assigned_tasks.all().order_by('due_date')
    else:
        tasks_list = request.user.assigned_tasks.filter(project__name=project).order_by('due_date')
    
    teams_list = request.user.membership_teams.all()
    status_list = Task.STATUS_CHOICES

    projects_list = []
    for team in teams_list:
        projects_list += team.projects.all()

    context = {
        'tasks': tasks_list,
        'projects': projects_list,
        'teams': teams_list,
        'statuses': status_list,
    }
    return render(request, 'projects/tasks.html', context)