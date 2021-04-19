from django.shortcuts import render

tasks = [
    {
        'project': 'Project 1', 
        'author': 'David',
        'name': 'Task 1', 
        'description': 'Task 1 oh', 
        'due_date': 'August 1, 2021',
        'status': 'Planteado',
        'assigned_members': ('Un', 'Dos')
    },
    {
        'project': 'Project 2', 
        'author': 'Aldo',
        'name': 'Task 2', 
        'description': 'Task 2 oh', 
        'due_date': 'August 31, 2021',
        'status': 'Planteado',
        'assigned_members': ('Un', 'Dos')
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