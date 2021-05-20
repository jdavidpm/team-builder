from django.contrib import messages
from django.shortcuts import redirect, render
from users.models import Task, User, Team, Project
from .forms import PersonalityTestForm
from json import loads
from urllib import request
from django.contrib.auth.decorators import login_required
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
		'bool': False 
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
	profile_results = User.objects.filter(first_name__icontains=query)
	team_results = Team.objects.filter(name__icontains=query)
	project_results = Project.objects.filter(name__icontains=query)
	total_results = list(chain(profile_results, project_results, team_results))
	paginator = Paginator(total_results, 2)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context = {
		'title': 'Resultados de búsqueda',
		'profile_results': profile_results,
		'team_results': team_results,
		'project_results': project_results,
		'page_obj': page_obj,
		'query': query
	}
	return render(request, 'layout/search_results.html', context)