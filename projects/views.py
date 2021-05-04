from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.models import Task, Team
from .forms import ProjectUpdateForm

@login_required
def projects_list(request):
    return render(request, 'projects/projects.html', {'title': 'Proyectos'})

@login_required
def project_item(request, id):
    project = request.user.created_projects.all().filter(id=id)
    if len(project):
        project = project[0]
        return render(request, 'projects/project.html', {'title': 'Proyecto - ' + str(project.name), 'project': project})
    else:
        return redirect('projects-list')

@login_required
def project_update(request, id):
    project = request.user.created_projects.all().filter(id=id)
    if len(project):
        project = project[0]
        if request.method == 'POST':
            u_form = ProjectUpdateForm(request.POST, instance=project)
            
            if u_form.is_valid():
                u_form.save()
                messages.success(request, f'¡El proyecto fue actualizada con éxito!')
                return redirect('projects-item', id=project.id)
        else:
            u_form = ProjectUpdateForm(instance=project)
        context = {
			'u_form': u_form,
			'title': 'Proyecto - ' + str(project.name)
		}
        return render(request, 'projects/project_update.html', context)
    else:
        return redirect('projects-list')
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