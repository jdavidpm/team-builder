from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserSignUpForm

def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡{username} tu cuenta fue creada con éxito! Ahora puedes iniciar sesión')
            return redirect('users-signin')
    else:
        form = UserSignUpForm()
    return render(request, 'users/signup.html', {'form': form, 'title': 'Registro'})

@login_required
def profile(request):
    return render(request, 'users/profile.html')