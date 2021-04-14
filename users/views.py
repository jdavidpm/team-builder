from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserSignUpForm

def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}')
            return redirect('layout-index')
    else:
        form = UserSignUpForm()
    return render(request, 'users/signup.html', {'form': form, 'title': 'Registro'})

def signin(request):
    return render(request, 'users/signin.html', {'title': 'Inicio de Sesión'})