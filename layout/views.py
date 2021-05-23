from django.contrib import messages
from django.shortcuts import redirect, render
from urllib import parse
from users.models import Task, User, Team, Project, Field, Profile
from .forms import PersonalityTestForm
from json import loads
from urllib import request
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from itertools import chain

data = None
with request.urlopen("https://jdavidpm.github.io/my-static-files/teamBuilder/json/hexaco_items.json") as url:
	data = loads(url.read().decode(encoding='utf-8'))

def index(request):
	tasks_list = Task.objects.all()
	context = {
		'tasks': tasks_list
	}
	return render(request, 'layout/index.html', context)

def faq(request):
	return render(request, 'layout/faq.html', {'title': 'Preguntas Frecuentes'})

def about(request):
	return render(request, 'layout/about.html', {'title': 'Acerca de'})

def notifications(request):
	return render(request, 'layout/notifications.html', {'title': 'Notificaciones'})

def tools(request):
	return render(request, 'layout/tools.html', {'title': 'Herramientas'})

@login_required
def hexaco_test(request):
	dict_facets = {'H':0, 'E':0, 'X':0, 'A':0, 'C':0, 'O':0}
	list_values = [1, 2, 3, 4, 5]
	if request.method == 'POST':
		form = PersonalityTestForm(request.POST)
		if form.is_valid():
			for i in range(1, 61):
				facet, sub_facet, is_reversed = data[i - 1]['statement_facet'].split(', ')
				statement_value = int(form.cleaned_data['statement_' + str(i)])
				dict_facets[facet] += list_values[-statement_value] if is_reversed == 'R' else statement_value
			dict_facets = {f: dict_facets[f] / 10 for f in dict_facets}
			current_user = request.user
			for f in dict_facets:
				setattr(current_user.profile, 'personality_' + f.lower(), dict_facets[f])
			current_user.save()
			return redirect('layout-hexaco-results')
	else:
		form = PersonalityTestForm()
	return render(request, 'layout/hexaco_test.html', {'title': 'Test de Personalidad', 'form': form})

@login_required
def hexaco_results(request):
	hexaco_caps = 'hexaco'
	chart_type = request.GET.get('type')
	labels = ['Honestidad', 'Emoción', 'Extraversión', 'Amabilidad', 'Escrupulosidad', 'Apertura']
	values = [getattr(request.user.profile, 'personality_' + c) for c in hexaco_caps]
	context = {
		'title': 'Resultados HEXACO',
		'labels': labels,
		'values': values,
		'type': chart_type if chart_type else 'polarArea',
		'bool': False,
		'height': '300' if chart_type == 'bar' else '550'
	}
	return render(request, 'layout/hexaco_results.html', context)

def hexaco_compare(request, username):
	user_compare = User.objects.filter(username=username)
	if len(user_compare):
		user_compare = user_compare[0]
		hexaco_caps = 'hexaco'
		labels = ['Honestidad', 'Emoción', 'Extraversión', 'Amabilidad', 'Escrupulosidad', 'Apertura']
		values_m = [getattr(request.user.profile, 'personality_' + c) for c in hexaco_caps]
		values_c = [getattr(user_compare.profile, 'personality_' + c) for c in hexaco_caps]
		context = {
			'title': 'Comparar HEXACO',
			'labels': labels,
			'values_m': values_m,
			'values_c': values_c,
			'compare_user': user_compare.first_name
		}
		return render(request, 'layout/hexaco_compare.html', context)
	return redirect('layout-hexaco-results')
	

def search_results(request):
	query = request.GET.get('q')
	sampleSize, hasProjects, hasTeams = request.GET.get('sampleSize'), request.GET.get('hasProjects'), request.GET.get('hasTeams')
	sampleSize = sampleSize if sampleSize else '5'
	hasProjects = hasProjects if hasProjects else 'Sí'

	interest_dict = []
	{interest_dict.append(v) for q, v in request.GET.items() if q.startswith('interest_')}

	experience_dict = []
	{experience_dict.append(v) for q, v in request.GET.items() if q.startswith('experience_')}

	field_dict = []
	{field_dict.append(v) for q, v in request.GET.items() if q.startswith('field_')}

	profile_query_qs, project_query_qs = Q(), Q()
	profile_results, team_results, project_results = [], [], []
	if len(interest_dict):
		for i in interest_dict:
			profile_query_qs = profile_query_qs | Q(interests=Field.objects.filter(name__icontains=i)[0])
		profile_results = Profile.objects.filter(profile_query_qs)
	
	if len(experience_dict):
		for i in experience_dict:
			profile_query_qs = profile_query_qs | Q(experience=Field.objects.filter(name__icontains=i)[0])
		profile_results = Profile.objects.filter(profile_query_qs)
	
	if len(field_dict):
		for i in field_dict:
			project_query_qs = project_query_qs | Q(fields=Field.objects.filter(name__icontains=i)[0])
		project_results = Project.objects.filter(project_query_qs)


	profile_results = User.objects.filter(Q(first_name__icontains=query) | Q(profile__in=profile_results)).distinct()
	team_results = Team.objects.filter(name__icontains=query).distinct()
	project_results = Project.objects.filter(Q(name__icontains=query)|project_query_qs).distinct()
	total_results = list(chain(profile_results, project_results if hasProjects == 'Sí' else [], team_results if hasTeams == 'Sí' else []))

	paginator = Paginator(total_results, int(sampleSize) if sampleSize else 5)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)



	context = {
		'title': 'Resultados de búsqueda',
		'page_obj': page_obj,
		'query': query,
		'sampleSize': sampleSize,
		'hasProjects': hasProjects,
		'hasTeams': hasTeams,
		'interest_dict': interest_dict,
		'experience_dict': experience_dict,
		'field_dict': field_dict
	}
	return render(request, 'layout/search_results.html', context)