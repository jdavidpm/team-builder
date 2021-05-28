from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.core.mail import send_mail
from .models import Student, Teacher
from .forms import UserSignUpForm, UserUpdateForm, ProfileUpdateForm, StudentProfileForm, TeacherProfileForm, StudentUpdateForm, TeacherUpdateForm
from .utils import *
from django.conf import settings
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string

def logout_required(function=None, logout_url=settings.LOGOUT_URL):
	actual_decorator = user_passes_test(
		lambda u: not u.is_authenticated,
		login_url=logout_url
	)
	if function:
		return actual_decorator(function)
	return actual_decorator

@logout_required
def signup(request, *args, **kwargs):
	if request.method == 'POST':
		u_form = UserSignUpForm(request.POST)
		if u_form.is_valid():
			email = u_form.cleaned_data.get('email')
			if User.objects.filter(email__iexact=email).count() == 0:
				user = u_form.save(commit=False)
				user.is_active = False
				user.save()
				current_site = get_current_site(request)
				mail_subject = 'Activa tu cuenta - Team Builder'
				message = render_to_string('users/email_template.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        })
				to_email = u_form.cleaned_data.get('email')
				send_mail(mail_subject, message, 'youremail', [to_email])
			#messages.success(request, f'¡Tu cuenta fue creada con éxito! Ahora puedes iniciar sesión y completar tu perfil')
				messages.warning(request, f'Se te envió un correo eléctronico para activar tu cuenta.')
				return redirect('users-update-profile', username=user.username)
	else:
		u_form = UserSignUpForm()
	context = {
		'u_form': u_form,
		'title': 'Registro'
	}
	return render(request, 'users/signup.html', context)

def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		messages.success(request, f'¡Tu cuenta fue activada con éxito! Ahora puedes iniciar sesión y completar tu perfil')
		return redirect('users-update-profile', username=user.username)
	else:
		messages.error(request, f'No fue posible activar tu cuenta. Por favor revisa el enlace de activación.')
		return redirect('users-update-profile', username=user.username)

@login_required
def profile(request, username):
	fields, users = [], []
	if username == request.user.username:
		users = User.objects.all().exclude(username=request.user.username)
		for field in request.user.profile._meta.many_to_many:
			if bool(getattr(request.user.profile, field.name).all()):
				fields.append({'name': names[field.name][0], 'values': getattr(request.user.profile, field.name).all(), 'icon': names[field.name][1]})
		return render(request, 'users/profile.html', {'title': request.user.first_name, 'fields': fields, 'users': users})
	else:
		users = User.objects.all().exclude(username=username)
		foreign_user = User.objects.filter(username=username).first()
		for field in foreign_user.profile._meta.many_to_many:
			if bool(getattr(foreign_user.profile, field.name).all()):
				fields.append({'name': names[field.name][0], 'values': getattr(foreign_user.profile, field.name).all(), 'icon': names[field.name][1]})
		return render(request, 'users/foreign_profile.html', {'title': foreign_user.first_name, 'foreign_user': foreign_user, 'fields': fields, 'users': users})

@login_required
def update_profile(request, username):
	if username == request.user.username:
		if request.method == 'POST':
			u_form = UserUpdateForm(request.POST, instance=request.user)
			p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
			if u_form.is_valid() and p_form.is_valid():
				u_form.save()
				p_form.save()
				if request.POST.get('school_role') == 'student' and not len(Student.objects.filter(user=request.user)):
					new_student = Student(user = request.user)
					new_student.save()
				elif request.POST.get('school_role') == 'teacher' and not len(Teacher.objects.filter(user=request.user)):
					new_teacher = Teacher(user = request.user)
					new_teacher.save()
				messages.success(request, f'¡Tu cuenta fue actualizada con éxito!')
				return redirect('users-profile', username=request.user.username)
		else:
			if not len(request.user.profile.experience.all()) and not len(request.user.profile.interests.all()):
				messages.warning(request, f'Por favor completa tu perfil.')
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

@login_required
def update_profile_school(request, username):
	if request.method == 'POST':
		if request.user.profile.school_role == 'student':
			if len(Student.objects.filter(user=request.user)):
				s_form = StudentUpdateForm(request.POST, instance=request.user.student_profile, initial={'user': request.user})
			else:
				s_form = StudentProfileForm(request.POST, initial={'user': request.user})
			if s_form.is_valid():
				s_form.save()
				messages.success(request, f'¡Tu perfil ha sido actualizado con éxito!')
				return redirect('users-profile', username=request.user.username)
		elif request.user.profile.school_role == 'teacher':
			if len(Teacher.objects.filter(user=request.user)):	
				s_form = TeacherUpdateForm(request.POST, instance=request.user.teacher_profile, initial={'user': request.user})
			else:
				s_form = TeacherProfileForm(request.POST, initial={'user': request.user})
			if s_form.is_valid():
				s_form.save()
				messages.success(request, f'¡Tu perfil ha sido actualizado con éxito!')
				return redirect('users-profile', username=request.user.username)
		else:
			return redirect('users-update', username=request.user.username)
	else:
		if request.user.profile.school_role == 'student':
			try:
				s_form = StudentUpdateForm(instance=request.user.student_profile, initial={'user': request.user})
			except:
				s_form = StudentProfileForm(initial={'user': request.user})
		elif request.user.profile.school_role == 'teacher':
			try:
				s_form = TeacherUpdateForm(instance=request.user.teacher_profile, initial={'user': request.user})
			except:
				s_form = TeacherProfileForm(initial={'user': request.user})
		else:
			messages.warning(request, f'Necesitas modificar tu rol en tu perfil para acceder a este formulario.')
			return redirect('users-update-profile', username=request.user.username)
	context = {
		'title': 'Datos Escolares',
		's_form': s_form,
	}
	return render(request, 'users/update_profile_school.html', context)