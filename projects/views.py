from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.models import Task, Team, Project
from django.utils import timezone
from .forms import ProjectUpdateForm
from django.http import HttpResponseNotFound

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
    user_teams = request.user.membership_teams.all()
    user_projects = []
    filter_object = None
    for team in user_teams:
        user_projects += team.projects.all()
    if not filter_by:
        tasks_list = []
        for project in user_projects:
            tasks_list += list(project.task_set.all()) # += list(project.task_set.all()) ?
    elif filter_by == "project":
        filter_object = get_object_or_404(Project, pk=object_id)
        if filter_object not in user_projects:
            return HttpResponseNotFound()
        tasks_list = list(filter_object.task_set.all()) # = list(filter_object.task_set.all()) ?
    elif filter_by == "team":
        filter_object = get_object_or_404(Team, pk=object_id)
        if filter_object not in user_teams:
            return HttpResponseNotFound()
        tasks_list = []
        for project in filter_object.projects.all():
            tasks_list += list(project.task_set.all()) # += list(project.task_set.all()) ?
    
    tasks_list.sort(key=lambda x: x.due_date)
    pending_tasks = [task for task in tasks_list if task.status == 'pendiente']
    in_dev_tasks = [task for task in tasks_list if task.status == 'en desarrollo']
    in_review_tasks = [task for task in tasks_list if task.status == 'en revision']
    completed_tasks = [task for task in tasks_list if task.status == 'completada']
    
    context = {
        'pending_tasks': {
            "everyoneOnTeam": pending_tasks,
            "user": [task for task in pending_tasks if request.user in task.assigned_members.all()]
        },
        'in_dev_tasks': {
            "everyoneOnTeam": in_dev_tasks,
            "user": [task for task in in_dev_tasks if request.user in task.assigned_members.all()]
        },
        'in_review_tasks': {
            "everyoneOnTeam": in_review_tasks,
            "user": [task for task in in_review_tasks if request.user in task.assigned_members.all()]
        },
        'completed_tasks': {
            "everyoneOnTeam": completed_tasks,
            "user": [task for task in completed_tasks if request.user in task.assigned_members.all()]
        },
        'projects': user_projects,
        'teams': user_teams,
        'statuses': Task.STATUS_CHOICES,
        'filter_object': filter_object,
        'timezone_now': timezone.now(),
    }
    return render(request, 'projects/tasks.html', context)