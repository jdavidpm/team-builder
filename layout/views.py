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
	if not request.user.is_authenticated:
		return render(request, 'layout/index.html', context)
	else:
		if request.user.profile.personality_h:
			return render(request, 'layout/index.html', context)
		else:
			messages.warning(request, f'Necesitas completar el test para usar la plataforma.')
			return redirect('layout-hexaco-test')
def faq(request):
	return render(request, 'layout/faq.html', {'title': 'Preguntas Frecuentes'})

def about(request):
	return render(request, 'layout/about.html', {'title': 'Acerca de'})

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
	if len(user_compare) and not user_compare[0].profile.results_private:
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
	query = query if query else '¬'
	message_info = None
	sampleSize, hasProjects, hasTeams = request.GET.get('sampleSize'), request.GET.get('hasProjects'), request.GET.get('hasTeams')
	sampleSize = sampleSize if sampleSize else '5'
	hasProjects = hasProjects if hasProjects else 'Sí'

	interest_dict = []
	{interest_dict.append(v) for q, v in request.GET.items() if q.startswith('interest_')}
	dict_inte = {q:v for q, v in request.GET.items() if q.startswith('interest_')}

	experience_dict = []
	{experience_dict.append(v) for q, v in request.GET.items() if q.startswith('experience_')}
	dict_expe = {q:v for q, v in request.GET.items() if q.startswith('experience_')}

	field_dict = []
	{field_dict.append(v) for q, v in request.GET.items() if q.startswith('field_')}
	dict_fiel = {q:v for q, v in request.GET.items() if q.startswith('field_')}

	profile_query_qs, project_query_qs = Q(), Q()
	profile_results, team_results, project_results = [], [], []
	if len(interest_dict):
		for i in interest_dict:
			field_query = None
			if len(Field.objects.filter(name__icontains=i)):
				field_query = Field.objects.filter(name__icontains=i)
				profile_query_qs = profile_query_qs | Q(interests=field_query[0])
				profile_results = Profile.objects.filter(profile_query_qs)
	
	if len(experience_dict):
		for i in experience_dict:
			field_query = None
			if len(Field.objects.filter(name__icontains=i)):
				field_query = Field.objects.filter(name__icontains=i)
				profile_query_qs = profile_query_qs | Q(experience=field_query[0])
				profile_results = Profile.objects.filter(profile_query_qs)
	
	if len(field_dict):
		for i in field_dict:
			field_query = Field.objects.filter(name__icontains=i)
			if len(field_query):
				project_query_qs = project_query_qs | Q(fields=field_query[0])

	profile_results = User.objects.filter(Q(first_name__icontains=query) | Q(profile__in=profile_results)).distinct()
	team_results = Team.objects.filter(Q(name__icontains=query)&Q(private=False)).distinct()
	if len(project_query_qs):
		project_results = Project.objects.filter((Q(name__icontains=query)|project_query_qs)).filter(Q(private=False)).distinct()
	else:
    		project_results = Project.objects.filter(Q(name__icontains=query)&Q(private=False))
	total_results = list(chain(profile_results, project_results if hasProjects == 'Sí' else [], team_results if hasTeams == 'Sí' else []))

	paginator = Paginator(total_results, int(sampleSize) if sampleSize else 5)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	if not len(page_obj):
		message_info = 'Tu búsqueda no dió ningún resultado.'

	str_page = '&'
	for i in dict_inte.keys():
		str_page += (i + '=' + dict_inte[i] + '&') 
	for i in dict_expe.keys():
		str_page += (i + '=' + dict_expe[i] + '&')
	for i in dict_fiel.keys():
		str_page += (i + '=' + dict_fiel[i] + '&') 
	context = {
		'title': 'Resultados de búsqueda',
		'page_obj': page_obj,
		'query': query,
		'sampleSize': sampleSize,
		'hasProjects': hasProjects,
		'hasTeams': hasTeams,
		'interest_dict': interest_dict,
		'experience_dict': experience_dict,
		'field_dict': field_dict,
		'message_info': message_info,
		'url_rest': str_page[:-1]
	}
	return render(request, 'layout/search_results.html', context)
def token_load(request):
	return render(request, 'layout/loaderio-4e678146c7228bcfb2f2028d48831e29.html')