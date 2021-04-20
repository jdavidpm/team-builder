from django.shortcuts import render
from users.models import Task

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