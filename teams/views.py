from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from users.models import Team, Profile, Field, Tool, Framework, Language, Distribution, TeamEvaluation
from .forms import TeamUpdateForm, TeamCreateForm, TeamMembersForm, TeamEvaluationForm
from django.db.models import Q
from json import loads
from urllib import request
from .utils import *

data = None
with request.urlopen("https://jdavidpm.github.io/my-static-files/teamBuilder/json/team_performance.json") as url:
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
			team_eval = TeamEvaluation()
			for f in dict_processes:
				setattr(team_eval, 'evaluation_' + f.lower(), dict_processes[f])
			team_eval.team = team
			team_eval.user = request.user
			team_eval.save()
			# send confirmation message to frontend
			return redirect('teams-item', id=id)
	else:
		form = TeamEvaluationForm()
		
	return render(request, 'teams/team_evaluate.html', {'title': 'Auto-evaluación de desempeño de equipo', 'form': form})

def teams_join_invitation(request):
	id_receiver = request.GET.get('toReceive')
	receiver_user = User.objects.filter(id=id_receiver)[0]
	current_user_teams = Team.objects.filter(founder=request.user)
	if receiver_user != request.user:
		context = {
			'title': 'Enviar solicitud a ' + receiver_user.first_name,
			'receiver_user': receiver_user,
			'current_user_teams': current_user_teams
		}
		return render(request, 'teams/teams_join_invitation.html', context)
	else:
		return redirect('users-profile', username=request.user.username) 	

def teams_join_invitation_done(request):
	user_to = User.objects.filter(username=request.GET.get('userTo'))[0]
	team_to = Team.objects.filter(name=request.GET.get('emailTeamInvite'))[0]
	send_email_invite(request.GET.get('emailSubject'),request.GET.get('messagePersonalized'), request.GET.get('emailFrom'), [request.GET.get('emailTo')], fail_silently=False)

	create_invitation(user_to, request.user, team_to)

	context = {
		'title': 'Invitación enviada',
		'user_to': user_to,
		'team_to': team_to
	}
	return render(request, 'teams/teams_join_invitation_done.html', context)

def teams_join_request(request):
	team_respond = request.GET.get('teamRespond')
	respond_request = request.GET.get('respondRequest')
	action = request.GET.get('action')
	if team_respond:
		team_instance = Team.objects.filter(name=team_respond)[0]
		if action == 'Responder':
			if respond_request == 'Aceptar':
				team_instance.members.set(list(team_instance.members.all()) + [request.user])
			else:
				delete_invitation(request.user, team_instance)
		elif action == 'Salir':
			team_instance.members.remove(request.user)
	return render(request, 'teams/teams_join_request.html')

def teams_creation(request):
	action = request.GET.get('action')
	team_size = request.GET.get('teamSize')
	message_info = False

	interest_dict = []
	{interest_dict.append(v) for q, v in request.GET.items() if q.startswith('interest_')}

	experience_dict = []
	{experience_dict.append(v) for q, v in request.GET.items() if q.startswith('experience_')}

	language_dict = []
	{language_dict.append(v) for q, v in request.GET.items() if q.startswith('language_')}

	framework_dict = []
	{framework_dict.append(v) for q, v in request.GET.items() if q.startswith('framework_')}

	distribution_dict = []
	{distribution_dict.append(v) for q, v in request.GET.items() if q.startswith('distribution_')}

	tool_dict = []
	{tool_dict.append(v) for q, v in request.GET.items() if q.startswith('tool_')}

	members_suggested = []
	if action:
		profile_query_qs = Q()
		if len(interest_dict):
			for i in interest_dict:
				query = Field.objects.filter(name__icontains=i)
				if query:
					profile_query_qs = profile_query_qs | Q(interests=query[0])
		if len(experience_dict):
			for i in experience_dict:
				query = Field.objects.filter(name__icontains=i)
				if query:
					profile_query_qs = profile_query_qs | Q(experience=query[0])
		if len(language_dict):
			for i in language_dict:
				query = Language.objects.filter(name__icontains=i)
				if query:
					profile_query_qs = profile_query_qs | Q(languages=query[0])
		if len(framework_dict):
			for i in framework_dict:
				query = Framework.objects.filter(name__icontains=i)
				if query:
					profile_query_qs = profile_query_qs | Q(frameworks=query[0])
		if len(distribution_dict):
			for i in distribution_dict:
				query = Distribution.objects.filter(name__icontains=i)
				if query:
					profile_query_qs = profile_query_qs | Q(distributions=query[0])
		if len(tool_dict):
			for i in tool_dict:
				query = Tool.objects.filter(name__icontains=i)
				if query:
					profile_query_qs = profile_query_qs | Q(sw_tools=query[0])
					profile_query_qs = profile_query_qs | Q(hw_tools=query[0])
		if len(profile_query_qs):
			members_suggested = Profile.objects.filter(profile_query_qs)
		else:
			message_info = 'Tu búsqueda no dió ningún resultado.'
		members_suggested = User.objects.filter(Q(profile__in=members_suggested)).distinct()
		if action == 'Crear':
			new_team_name = request.GET.get('newTeamName') if request.GET.get('newTeamName') else 'No se nombró a tu equipo'
			if not Team.objects.filter(name=new_team_name):	
				new_team = Team(founder=request.user, name=new_team_name)
				new_team.save()
				new_team.members.set(members_suggested[:int(team_size)])
				new_team.members.add(request.user)
				return redirect('teams-list')
			else:
				messages.error(request, f'Ese nombre ya existe')
	else:
		message_info = 'Para poder formar un equipo ocupa al menos dos de los filtros mostrados arriba.'
	context = {
		'title': 'Formación de Equipos', 
		'message_info': message_info,
		'interest_dict': interest_dict,
		'experience_dict': experience_dict,
		'language_dict': language_dict,
		'framework_dict': framework_dict,
		'distribution_dict': distribution_dict,
		'tool_dict': tool_dict,
		'members_suggested': members_suggested[:int(team_size if team_size else 0)],
		'teamSize': team_size
	}
	return render(request, 'teams/teams_creation.html', context)