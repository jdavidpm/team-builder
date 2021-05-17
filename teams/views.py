from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import Team
from .forms import TeamUpdateForm, TeamCreateForm, TeamMembersForm, TeamEvaluationForm
from json import loads
from urllib import request

data = None
with request.urlopen("https://raw.githubusercontent.com/jdavidpm/team-builder/master/static/json/team_performance.json") as url:
	data = loads(url.read().decode(encoding='utf-8'))

@login_required
def teams(request):
	return render(request, 'teams/teams.html', {'title': 'Equipos'})

@login_required
def teams_item(request, id):
	team = request.user.membership_teams.all().filter(id=id)
	if len(team):
		team = team[0]
		return render(request, 'teams/team.html', {'title': 'Equipo - ' + str(team.name), 'team': team})
	else:
		return redirect('teams-list')

@login_required
def team_update(request, id):
	team = request.user.membership_teams.all().filter(id=id)
	if len(team):
		team = team[0]
		if request.method == 'POST':
			u_form = TeamUpdateForm(request.POST, instance=team)
			
			if u_form.is_valid():
				u_form.save()
				messages.success(request, f'¡El equipo fue actualizada con éxito!')
				return redirect('teams-item', id=team.id)
		else:
			u_form = TeamUpdateForm(instance=team)
		context = {
			'u_form': u_form,
			'title': 'Actualizar Equipo - ' + str(team.name)
		}
		return render(request, 'teams/team_update.html', context)
	else:
		return redirect('teams-list')

@login_required
def team_create(request): 
	if request.method == 'POST':
		c_form = TeamCreateForm(request.POST, initial={'founder': request.user})
		if c_form.is_valid():
			obj = c_form.save()
			obj.members.set([request.user])
			obj.save()
			messages.success(request, f'¡El equipo fue creado con éxito!')
			return redirect('teams-update-members', id=obj.id)
	else:
		c_form = TeamCreateForm(initial={'founder': request.user})
	context = {
		'c_form': c_form,
		'title': 'Crear equipo'
	}
	return render(request, 'teams/team_create.html', context)

@login_required
def team_update_members(request, id):
	team = request.user.membership_teams.all().filter(id=id)
	if len(team):
		team = team[0]
		if request.method == 'POST':
			m_form = TeamMembersForm(request.POST)
			if m_form.is_valid():
				team.members.set(m_form.cleaned_data['members'])
				team.save()
				messages.success(request, f'¡El equipo fue actualizada con éxito!')
				return redirect('teams-item', id=team.id)
		else:
			m_form = TeamMembersForm(instance=team)
		context = {
			'm_form': m_form,
			'title': 'Actualizar Equipo - ' + str(team.name)
		}
		return render(request, 'teams/team_update_members.html', context)
	else:
		return redirect('teams-list')
		
def team_evaluate(request, id):
	dict_processes = {'p1':0, 'p2':0, 'p3':0, 'p4':0, 'p5':0, 'p6':0, 'p7':0}
	processes_questions_count = {'p1':0, 'p2':0, 'p3':0, 'p4':0, 'p5':0, 'p6':0, 'p7':0}
	
	if request.method=='POST':
		form = TeamEvaluationForm(request.POST)
		if form.is_valid():
			for i in range(1, 19):
				process_name, process = data[i - 1]['statement_category'].split(', ')
				dict_processes[process] += int(form.cleaned_data['statement_' + str(i)])
				processes_questions_count[process] += 1
			dict_processes = {f: dict_processes[f] / processes_questions_count[f] for f in dict_processes}
			team = get_object_or_404(Team, pk=id)
			print(team.name)

			for f in dict_processes:
				setattr(team, 'evaluation_' + f.lower(), dict_processes[f])
			team.save()
			return redirect('layout-index')
	else:
		form = TeamEvaluationForm()
		
	return render(request, 'teams/team_evaluate.html', {'title': 'Auto-evaluación de desempeño de equipo', 'form': form})