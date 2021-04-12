from django.shortcuts import render

tasks = [
    {
        'author': 'David',
        'title': 'Task 1', 
        'date': 'August 1, 2021',
        'deadline': 'August 13, 2021'
    },
    {
        'author': 'Aldo',
        'title': 'Task 2', 
        'date': 'August 1, 2021',
        'deadline': 'August 13, 2021'
    }
]

def index(request):
    context = {
        'tasks': tasks
    }
    return render(request, 'layout/index.html', context)

def faq(request):
    return render(request, 'layout/faq.html', {'title': 'Preguntas Frecuentes'})