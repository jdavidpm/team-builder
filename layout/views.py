from django.shortcuts import redirect, render
from users.models import Task
from .forms import NameForm

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

def tools(request):
    return render(request, 'layout/tools.html', {'title': 'Herramientas'})

def hexaco_test(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            return redirect('layout-index')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
    return render(request, 'layout/hexaco_test.html', {'title': 'Test de Personalidad', 'form': form})