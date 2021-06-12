from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.models import Task, TaskActivity, Team, Project, User, ResourceURL, Notification
from django.utils import timezone
from .forms import ProjectUpdateForm, ProjectCreateForm, TaskForm, NewTaskForm, ResourceURLForm
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse

@login_required
def projects_list(request):
	return render(request, 'projects/projects.html', {'title': 'Proyectos'})

@login_required
def project_item(request, id):
    project = request.user.created_projects.all().filter(id=id)
    if len(project):
        project = project[0]
        resources_url = ResourceURL.objects.filter(project=project)
        context = {
            'title': 'Proyecto - ' + str(project.name), 
            'project': project,
            'resources_url': resources_url
        }
        return render(request, 'projects/project.html', context)
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
			'title': 'Proyecto - ' + str(project.name),
            'project_id': id
		}
		return render(request, 'projects/project_update.html', context)
	else:
		return redirect('projects-list')

@login_required
def projects_create(request): 
	if request.method == 'POST':
		c_form = ProjectCreateForm(request.POST, initial={'author': request.user})
		
		if c_form.is_valid():
			c_form.save()
			messages.success(request, f'¡El proyecto fue creado con éxito!')
			return redirect('projects-list')
	else:
		c_form = ProjectCreateForm(initial={'author': request.user})
	context = {
		'c_form': c_form,
		'title': 'Crear proyecto'
	}
	return render(request, 'projects/project_create.html', context)
		
@login_required
def tasks(request):
	return filtered_tasks(request)

@login_required
def filtered_tasks(request, filter_by="", object_id=""):
    # team and project objects for the sidebar menu
    user_teams = request.user.membership_teams.all()
    user_projects = []
    filter_object = None
    for team in user_teams:
        user_projects += [project for project in team.projects.all() if project not in user_projects]
    
    if not filter_by:
        tasks_list = []
        for project in user_projects:
            tasks_list += list(project.task_set.all())
    elif filter_by == "project":
        filter_object = get_object_or_404(Project, pk=object_id)
        if filter_object not in user_projects:
            return HttpResponseNotFound()
        tasks_list = list(filter_object.task_set.all())
    elif filter_by == "team":
        filter_object = get_object_or_404(Team, pk=object_id)
        if filter_object not in user_teams:
            return HttpResponseNotFound()
        tasks_list = []
        for project in filter_object.projects.all():
            tasks_list += list(project.task_set.all())
    
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


def saveTaskActivity(on_task, by_user, with_description, recipients):
    print("on savetaskactivity function")
    new_task_activity = TaskActivity(
        task = on_task,
        user = by_user,
        description = with_description
    )
    new_task_activity.save()
    for recipient in recipients:
        if recipient != by_user:
            new_notification = Notification(
                user = recipient,
                category = f'Actividad en la tarea "{on_task}" del proyecto "{on_task.project}"',
                text = with_description,
                task_activity = new_task_activity
            )
            new_notification.save()

@login_required
def updateTask(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # Verify access by teams working on the task project (only members of the teams working on the task project can view the task)
    user_teams = request.user.membership_teams.all()
    user_projects = []
    for team in user_teams:
        user_projects += [project for project in team.projects.all() if project not in user_projects]
    if task.project not in user_projects:
        return HttpResponseNotFound()

    # custom queryset for assigned_members options (only members of the teams working on the project)
    teams_in_project = task.project.team_set.all()
    members = User.objects.none()
    for team in teams_in_project:
        members |= team.members.all()
    form = TaskForm(instance=task, team_members=members)
    data = form.data

    if request.method=='POST':
        form = TaskForm(request.POST, instance=task, initial=data)
        if form.is_valid():
            if form.has_changed():
                for field in form.changed_data:
                    if field == 'name':
                        description = f"{request.user} cambió el nombre de la tarea \"{form.initial['name']}\" a \"{form.cleaned_data['name']}\""
                    if field == 'description':
                        description = f"{request.user} actualizó la descripción de la tarea \"{form.cleaned_data['name']}\""
                    if field == 'status':
                        if form.cleaned_data['status'] == 'pendiente':
                            status = 'Pendiente'
                        elif form.cleaned_data['status'] == 'en desarrollo':
                            status = "En desarrollo"
                        if form.cleaned_data['status'] == 'en revision':
                            status = "Lista para revisión"
                        if form.cleaned_data['status'] == 'completada':
                            status = "Completada"
                        description = f"{request.user} actualizó el estado de la tarea \"{form.cleaned_data['name']}\" a: {status}"
                    if field == 'due_date':
                        description = f"{request.user} actualizó la fecha de vencimiento de la tarea \"{form.cleaned_data['name']}\" a: {form.cleaned_data['due_date'].strftime('%x %X')}"
                    if field == 'assigned_members':
                        new_assigned_members = [str(member) for member in form.cleaned_data['assigned_members']]
                        description = f"{request.user} asignó la tarea \"{form.cleaned_data['name']}\" a: {'%s' % ', '.join(new_assigned_members)}"
                    saveTaskActivity(
                        task,
                        request.user,
                        description,
                        members.distinct()
                    )
            form.save()
            messages.success(request, f'¡La tarea fue actualizada con éxito!')
        else:
            messages.error(request, f'Error al actualizar la tarea. Comprueba los campos e intenta de nuevo.')
        return HttpResponseRedirect(reverse('projects-update_task', kwargs={'pk': task.id }))

    context = {
        'task_form': form,
        'projects': user_projects,
        'teams': user_teams,
        'task': task
    }
    return render(request, 'projects/task_update.html', context)

@login_required
def createTask(request, project_id):
    # team and project objects for the sidebar menu
    user_teams = request.user.membership_teams.all()
    user_projects = []
    for team in user_teams:
        user_projects += [project for project in team.projects.all() if project not in user_projects]

    # custom queryset for assigned_members options (only members of the teams working on the project)
    project = get_object_or_404(Project, pk=project_id)
    teams_in_project = project.team_set.all()
    members = User.objects.none()
    for team in teams_in_project:
        members |= team.members.all()
    #form = NewTaskForm(team_members=members)
    form = NewTaskForm(team_members=members)

    if request.method=='POST':
        form = NewTaskForm(request.POST, initial={'project': project, 'author': request.user}, team_members=members)
        
        if form.is_valid():
            new_task = form.save()
            saveTaskActivity(
                new_task,
                request.user,
                f'{request.user} creó la tarea "{new_task}" en el proyecto "{new_task.project}"',
                members.distinct()
            )
            messages.success(request, f'¡La tarea fue creada con éxito!')
            return HttpResponseRedirect(reverse('projects-tasks'))
        else:
            messages.error(request, f'Error al crear la tarea. Comprueba los campos e intenta de nuevo.')
            return render(request, 'projects/task_create.html', {
                'task_form': form,
                'projects': user_projects,
                'teams': user_teams,
                'task_project': project   
            })

    context = {
        'task_form': form,
        'projects': user_projects,
        'teams': user_teams,
        'task_project': project
    }
    return render(request, 'projects/task_create.html', context)


@login_required
def deleteTask(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.author != request.user:
        return HttpResponseNotFound()
    if request.method == 'POST':
        task.delete()
        messages.success(request, f'¡La tarea fue eliminada con éxito!')
        return HttpResponseRedirect(reverse('projects-tasks'))
    context = {'task': task}
    return render(request, 'projects/task_delete.html', context)

def projects_resource_add(request):
    project = request.user.created_projects.all().filter(id=request.GET.get('id'))
    if request.method == 'POST':
        form = ResourceURLForm(request.POST, initial={'project': project})
        if form.is_valid():
            form.save()
            messages.success(request, f'¡El recurso fue creado con éxito!')
            return redirect('projects-list')
    else:
        form = ResourceURLForm(initial={'project': project})
    context = {
        'title': 'Agregar Recurso',
        'form': form
    }
    return render(request, 'projects/projects_resource_add.html', context)
