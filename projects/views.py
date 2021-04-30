from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import Task, Team

@login_required
def projects(request):
    projects_list = request.user.created_projects.all()
    return render(request, 'projects/projects.html', {'title': 'Proyectos', 'projects_list': projects_list})


@login_required
def tasks(request):
    return filtered_tasks(request)

@login_required
def filtered_tasks(request, filter_by="", object_id=""):
    if not filter_by:
        tasks_list = request.user.assigned_tasks.all().order_by('due_date')
    elif filter_by == "project":
        tasks_list = request.user.assigned_tasks.filter(project__id=object_id).order_by('due_date')
    elif filter_by == "team":
        team = Team.objects.get(pk=object_id)
        tasks_list = []
        for project in team.projects.all():
            tasks_list += [task for task in project.task_set.all() if request.user in task.assigned_members.all()]
            tasks_list.sort(key=lambda x: x.due_date)
    
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