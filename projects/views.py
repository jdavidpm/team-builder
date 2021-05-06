from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.models import Task, Team, Project
from django.utils import timezone
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
        filter_string = ""
    elif filter_by == "project":
        tasks_list = request.user.assigned_tasks.filter(project__id=object_id).order_by('due_date')
        filter_string = Project.objects.get(pk=object_id).name
    elif filter_by == "team":
        team = Team.objects.get(pk=object_id)
        tasks_list = []
        for project in team.projects.all():
            tasks_list += [task for task in project.task_set.all() if request.user in task.assigned_members.all()]
            tasks_list.sort(key=lambda x: x.due_date)
        filter_string = team.name
    elif filter_by == "status":
        status_string = Task.STATUS_CHOICES[object_id][0]
        tasks_list = request.user.assigned_tasks.filter(status=status_string).order_by('due_date')
        filter_string = status_string

    teams_list = request.user.membership_teams.all()
    projects_list = []
    for team in teams_list:
        projects_list += team.projects.all()

    context = {
        'pending_tasks': [task for task in tasks_list if task.status == 'pendiente'],
        'in_dev_tasks': [task for task in tasks_list if task.status == 'en desarrollo'],
        'in_review_tasks': [task for task in tasks_list if task.status == 'en revision'],
        'completed_tasks': [task for task in tasks_list if task.status == 'completada'],
        'projects': projects_list,
        'teams': request.user.membership_teams.all(),
        'statuses': Task.STATUS_CHOICES,
        'filter': filter_string,
        'timezone_now': timezone.now()
    }
    return render(request, 'projects/tasks.html', context)
