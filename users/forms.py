from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .widgets import ToggleWidget, PictureWidget

class UserSignUpForm(UserCreationForm):
	email = forms.EmailField(label=u'Correo Electrónico')

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email', 'username','password1', 'password2']
		labels = {
			'first_name': ('Nombre(s)'),
			'last_name': ('Apellidos'),
		}
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username','first_name', 'last_name', 'email']
		labels = {
			'first_name': ('Nombre(s)'),
			'last_name': ('Apellidos'),
		}

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		image = forms.ImageField()
		fields = ['school_register', 'distributions', 'experience', 'interests', 'languages', 'frameworks', 'sw_tools', 'hw_tools', 'image']
		widgets = {
			#'distributions' : forms.CheckboxSelectMultiple,
			#'experience' : forms.CheckboxSelectMultiple,
			#'interests' : forms.CheckboxSelectMultiple,
			#'languages' : forms.CheckboxSelectMultiple,
			#'frameworks' : forms.CheckboxSelectMultiple,
			#'sw_tools' : forms.CheckboxSelectMultiple,
			#'hw_tools' : forms.CheckboxSelectMultiple,
			'image': forms.widgets.FileInput
		}
		labels = {
			'school_register': ('Matrícula'),
			'distributions': ('Distros'),
			'sw_tools': ('Herramientas de Software'),
			'hw_tools': ('Herramientas de Hardware'),
			'experience': ('Experiencia'),
			'interests': ('Intereses'),
			'languages': ('Lenguajes de Programación'),
			'frameworks': ('Frameworks'),
			'image': ('Foto de Perfil')
		}
		help_texts = {
			'school_register': ('Número de boleta o equivalente.'),
		}

class JustAnotherForm(forms.Form): #Toggle Widget in use example
	working = forms.BooleanField(
		required=False,
		widget=ToggleWidget(
			options={
				'on': 'Yep',
				'off': 'Nope'
			}
		),
		label=u'Prueba'
	)
