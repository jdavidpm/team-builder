from django.shortcuts import render

tasks = [
    {
        'author': 'David',
        'title': 'Task 1', 
        'date': 'August 1, 2021',
        'deadline': 'August 13, 2021',
        'delegate': 'Aldo'
    },
    {
        'author': 'Aldo',
        'title': 'Task 2', 
        'date': 'August 1, 2021',
        'deadline': 'August 18, 2021',
        'delegate': 'David'
    }
]

def index(request):
    context = {
        'tasks': tasks
    }
    return render(request, 'layout/index.html', context)

def faq(request):
    return render(request, 'layout/faq.html', {'title': 'Preguntas Frecuentes'})

def about(request):
    return render(request, 'layout/about.html', {'title': 'Acerca de'})

def signin(request):
    return render(request, 'signin.html', {'title': 'Inicio de Sesión'})

def signup(request):
    return render(request, 'signup.html', {'title': 'Registro'})