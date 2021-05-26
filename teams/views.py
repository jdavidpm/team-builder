from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from users.models import Team, JoinInvitation, JoinRequest, Profile, Field, Tool, Framework, Language, Distribution, TeamEvaluation
from .forms import TeamUpdateForm, TeamCreateForm, TeamMembersForm, TeamEvaluationForm
from django.db.models import Q
from json import loads
from urllib import request
from .utils import *
from apriori_python import apriori
import tabulate

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
			
			# compute average evaluation for current team
			# if a user evaluated the team more than once, each evaluation will be considered for the team average evaluation (might be changed in a future update)
			evaluations = dict()
			for process in dict_processes:
				evaluations[process] = {'sum': 0, 'avg': 0}
			total_evaluations = len(team.teamevaluation_set.all())
			for evaluation in team.teamevaluation_set.all():
				for process, eval in evaluations.items():
					eval['sum'] += getattr(evaluation, 'evaluation_' + process)
			general_avg_sum = 0
			for process, eval in evaluations.items():
				eval['avg'] = eval['sum'] / total_evaluations
				general_avg_sum += eval['avg']
			team.average_eval = general_avg_sum / len(dict_processes)
			team.save()

			# -------- missing confirmation message here to frontend before returning --------

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

# association rules functions (there might be a better place to put all this stuff)
TEAMS_SAMPLE_FRACTION = 0.3 #(top TEAMS_SAMPLE_FRACTION % in performance evaluation)
MIN_TEAM_EVALUATORS = 1
IDEAL_SELECTED_FACET_SET_SIZE = 2
MIN_SUPPORT = 0.4
MIN_CONFIDENCE = 0.7
MIN_LIFT = 1.4
FACETS_MAP = ['h', 'e', 'x', 'a', 'c', 'o']

def has_enough_evaluators(team):
	evaluators = set()
	evaluations = team.teamevaluation_set.all()
	for evaluation in evaluations:
		evaluators.add(evaluation.user)
	# print("team: ", team)
	# print(evaluators)
	if len(evaluators) >= MIN_TEAM_EVALUATORS:
		return True
	else:
		return False

def has_enough_members(team):
	members = team.members.all()
	if len(members) >= 2:
		return True
	else:
		return False
	
def gen_association_rules():
	# get sample of teams with highest performance evaluations (top TEAMS_SAMPLE_FRACTION%)
	all_teams = list(Team.objects.exclude(average_eval__isnull=True).order_by('average_eval'))
	filtered_teams_1 = [team for team in all_teams if has_enough_members(team)]
	# print(filtered_teams_1)
	filtered_teams_2 = [team for team in filtered_teams_1 if has_enough_evaluators(team)]
	# print(filtered_teams_2)
	sample_size = len(filtered_teams_2) * TEAMS_SAMPLE_FRACTION
	print(f"sample size is: {sample_size}")
	if sample_size < 5:
		print('not enough teams in sample')
		return -1
	teams_sample = []
	for _ in range(int(sample_size)):
		teams_sample.append(filtered_teams_2.pop())
	# print("\nteam sample:")
	# print(teams_sample)
	
	# generate transactions as apriori algorithm input
	personalities_transactions = []
	for team in teams_sample:
		print(team)
		team_personalities = set()
		for member in team.members.all():
			# print(member)
			member_personalities = []
			for facet in FACETS_MAP:
				value = getattr(member.profile, 'personality_' + facet)
				# print("facet: ", facet, ", value: ", value)
				if value:
					threshold = value - 3
					member_personalities.append({'facet': facet, 'threshold': threshold})
				else:
					break
			if not member_personalities:
				break
			member_personalities = sorted(member_personalities, key = lambda i: abs(i['threshold']))
			# print(member_personalities)
			current_added_facets = 0
			while member_personalities:
				if abs(member_personalities[-1]['threshold']) == 2.0 or current_added_facets < IDEAL_SELECTED_FACET_SET_SIZE:
					facet_dict = member_personalities.pop()
					if facet_dict['threshold'] < 0:
						team_personalities.add('-'+facet_dict['facet'])
					else:
						team_personalities.add(facet_dict['facet'])
					current_added_facets += 1
				else:
					break
		# print("\n---------team facets-------------\n", team_personalities)
		if team_personalities:
			personalities_transactions.append(list(team_personalities))
	# print(personalities_transactions)
	if personalities_transactions:
		# get rules with apriori algorithm, it takes the transactions from where to extract rules, min support and min confidence
		freqItemSet, rules_list = apriori(personalities_transactions, minSup=MIN_SUPPORT, minConf=MIN_CONFIDENCE)
		dict_keys = ['antecedent', 'consecuent', 'confidence']
		rules = list()
		for index, rule in enumerate(rules_list):
			rule_dict = dict(zip(dict_keys, rule))
			
			# create new keys that are not present in rule_dict yet
			rule_dict['itemset_frequence'] = 0
			rule_dict['consecuent_frequence'] = 0

			rule_itemset = rule[0].union(rule[1])
			
			# calculate itemset_frecuence and consecuent_frecuence
			for transaction in personalities_transactions:
				if rule_itemset.issubset(transaction):
					rule_dict['itemset_frequence'] += 1
				if rule[1].issubset(transaction):
					rule_dict['consecuent_frequence'] += 1
			
			# create new keys and calculate and assign its values
			rule_dict['support'] = rule_dict['itemset_frequence'] / len(personalities_transactions)
			rule_dict['lift'] = rule_dict['confidence'] / (rule_dict['consecuent_frequence']/len(personalities_transactions))

			rules.append(rule_dict)
	else:
		return[]

	return [ rule for rule in rules if (rule['lift'] > MIN_LIFT) ]


def teams_creation(request):
	action = request.GET.get('action')
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
	recommended_members = []
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
		
		# Recommendations (implemented through a submit button so far)
		if action == 'Obtener recomendaciones':
			rules_list = gen_association_rules() # a list of dicts
			
			if len(rules_list) > 0:
				rules_list = sorted(rules_list, key = lambda i: (i['lift'], i['confidence'], i['support']))[::-1]
				header = rules_list[0].keys()
				rows = [rule.values() for rule in rules_list]
				print(tabulate.tabulate(rows, header))
				user_personalities = []
				selected_users_personalities = []
				for facet in FACETS_MAP:
					value = getattr(request.user.profile, 'personality_' + facet)
					if value == None:
						message_info = "Realiza primero la prueba HEXACO para obtener recomendaciones"
						context = {
							'title': 'Formación de Equipos', 
							'message_info': message_info,
							'interest_dict': interest_dict,
							'experience_dict': experience_dict,
							'language_dict': language_dict,
							'framework_dict': framework_dict,
							'distribution_dict': distribution_dict,
							'tool_dict': tool_dict,
							'members_suggested': members_suggested
						}
						return render(request, 'teams/teams_creation.html', context)
					
					# print("facet: ", facet, ", value: ", value)
					threshold = value - 3
					if threshold > 0:
						user_personalities.append({'facet': facet, 'threshold': threshold})
					else:
						user_personalities.append({'facet': '-'+facet, 'threshold': threshold})
				user_personalities = sorted(user_personalities, key = lambda i: abs(i['threshold']))
				selected_users_personalities.extend([user_personalities[-1]['facet'], user_personalities[-2]['facet']])
				# print(user_personalities)
				# print(selected_users_personalities)
				target_facets = []
				for rule in rules_list:
					for user_facet in selected_users_personalities:
						if user_facet in rule['antecedent']:
							# print(user_facet, " in ", rule['antecedent'])
							target_facets.extend([facet for facet in list(rule['consecuent']) if facet not in target_facets])
						elif user_facet in rule['consecuent']:
							# print(user_facet, " in ", rule['consecuent'])
							target_facets.extend([facet for facet in list(rule['antecedent']) if facet not in target_facets])
				# print("target facets: ", target_facets)

				
				# print(members_suggested)
				for member in members_suggested:
					member_personalities = []
					selected_member_personalities = []
					test_value = getattr(member.profile, 'personality_h')
					if test_value == None:
						break
					for facet in FACETS_MAP:
						value = getattr(member.profile, 'personality_' + facet)
						threshold = value - 3
						if threshold > 0:
							member_personalities.append({'facet': facet, 'threshold': threshold})
						else:
							member_personalities.append({'facet': '-'+facet, 'threshold': threshold})
					member_personalities = sorted(member_personalities, key = lambda i: abs(i['threshold']))
					selected_member_personalities.extend(
						[member_personalities[-1], member_personalities[-2]] # could add a 3rd facet to increase possibilities of being included in recommendations
					)
					# print(member_personalities)
					# print(selected_member_personalities)

					for selected_facet_dict in selected_member_personalities:
						if selected_facet_dict['facet'] in target_facets:
							recommended_members.append({'member': member, 'selected_facet': selected_facet_dict})
				# print("recommended: ")	
				# print(recommended_members)
				ids = []
				duplicates = []
				recommended_members = sorted(recommended_members, key = lambda i: abs(i['selected_facet']['threshold']))[::-1]
				recommended_members = [ member_dict['member'] for member_dict in recommended_members]
				for i, member in enumerate(recommended_members):
					if member.id in ids:
						duplicates.append(i)
					ids.append(member.id)
				for index in duplicates:
					recommended_members.pop(index)
				print("ordered recomended")
				print(recommended_members) # descending ordered members list (most recommended first)
					

			else:
				message_info = "Lo sentimos, no hay recomendaciones"
			
		if action == 'Formar':
			print(members_suggested)
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
		'members_suggested': members_suggested,
		'recommended_members': recommended_members
	}
	return render(request, 'teams/teams_creation.html', context)

