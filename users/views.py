from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserSignUpForm, UserUpdateForm, ProfileUpdateForm, JustAnotherForm
from django.contrib.auth.models import User
from django.conf import settings
from .utils import *

def logout_required(function=None, logout_url=settings.LOGOUT_URL):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=logout_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

@logout_required
def signup(request):
    if request.method == 'POST':
        u_form = UserSignUpForm(request.POST)
        if u_form.is_valid():
            u_form.save()
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
def profile(request, username):
    fields, users = [], []
    if username == request.user.username:
        users = User.objects.all().exclude(username='ssiet').exclude(username=request.user.username)
        for field in request.user.profile._meta.many_to_many:
            if bool(getattr(request.user.profile, field.name).all()):
                fields.append({'name': names[field.name][0], 'values': getattr(request.user.profile, field.name).all(), 'icon': names[field.name][1]})
        return render(request, 'users/profile.html', {'title': 'Perfil', 'fields': fields, 'users': users})
    else:
        users = User.objects.all().exclude(username='ssiet').exclude(username=username)
        foreign_user = User.objects.filter(username=username).first()
        for field in foreign_user.profile._meta.many_to_many:
            if bool(getattr(foreign_user.profile, field.name).all()):
                fields.append({'name': names[field.name][0], 'values': getattr(foreign_user.profile, field.name).all(), 'icon': names[field.name][1]})
        return render(request, 'users/foreign_profile.html', {'title': 'Perfil', 'foreign_user': foreign_user, 'fields': fields, 'users': users})

@login_required
def updateProfile(request, username):
    if username == request.user.username:
        if request.method == 'POST':
            o_form = JustAnotherForm()
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'¡Tu cuenta fue actualizada con éxito!')
                return redirect('users-profile', username=request.user.username)
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'u_form': u_form,
            'p_form': p_form,
            'title': 'Actualizar Perfil'
        }
        return render(request, 'users/update_profile.html', context)
    else:
        messages.warning(request, f'No tienes permiso para entrar a esta página')
        return redirect('layout-index')