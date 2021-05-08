from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TeamUpdateForm, TeamCreateForm

def teams(request):
	return render(request, 'teams/teams.html')

def teams_item(request, id):
	team = request.user.membership_teams.all().filter(id=id)
	if len(team):
		team = team[0]
		return render(request, 'teams/team.html', {'title': 'Equipo - ' + str(team.name), 'team': team})
	else:
		return redirect('teams-list')

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
			'title': 'Proyecto - ' + str(team.name)
		}
		return render(request, 'teams/team_update.html', context)
	else:
		return redirect('teams-list')

@login_required
def team_create(request): 
	if request.method == 'POST':
		c_form = TeamCreateForm(request.POST, initial={'founder': request.user, 'members': request.user})
		if c_form.is_valid():
			c_form.save()
			messages.success(request, f'¡El equipo fue creado con éxito!')
			return redirect('teams-list')
	else:
		c_form = TeamCreateForm(initial={'founder': request.user, 'members': request.user})
	context = {
		'c_form': c_form,
		'title': 'Crear equipo'
	}
	return render(request, 'teams/team_create.html', context)