from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserSignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        u_form = UserSignUpForm(request.POST)
        if u_form.is_valid():
            u_form.save()
            #p_form.save(commit=False)
            #p_form.user = user
            #p_form.save()
            #username = u_form.cleaned_data.get('username')
            messages.success(request, f'¡Tu cuenta fue creada con éxito! Ahora puedes iniciar sesión y completar tu perfil')
            return redirect('users-signin')
    else:
        u_form = UserSignUpForm()
    context = {
        'u_form': u_form,
        'title': 'Registro'
    }
    return render(request, 'users/signup.html', context)

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def updateProfile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'¡Tu cuenta fue actualizada con éxito!')
            return redirect('users-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Actualizar Perfil'
    }
    return render(request, 'users/update-profile.html', context)