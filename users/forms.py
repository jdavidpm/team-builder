from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
#from django.db.models import fields
from .models import Academy, Profile, Student, Subject, Teacher
from .widgets import ToggleWidget

class SignInFrom(AuthenticationForm):
	class Meta:
		model = User
		
class UserSignUpForm(UserCreationForm):
	email = forms.EmailField(label=u'Correo Electrónico')

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
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
		fields = ['first_name', 'last_name', 'username', 'email']
		labels = {
			'first_name': ('Nombre(s)'),
			'last_name': ('Apellidos'),
		}
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		image = forms.ImageField()
		fields = ['school_register', 'school_role', 'distributions', 'experience', 'interests', 'languages', 'frameworks', 'sw_tools', 'hw_tools', 'results_private', 'image']
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
			'school_role': ('Rol Escolar'),
			'distributions': ('Distros'),
			'sw_tools': ('Herramientas de Software'),
			'hw_tools': ('Herramientas de Hardware'),
			'experience': ('Experiencia'),
			'interests': ('Intereses'),
			'languages': ('Lenguajes de Programación'),
			'frameworks': ('Frameworks'),
			'results_private': ('Personalidad privada'),
			'image': ('Foto de Perfil')
		}
		help_texts = {
			'school_register': ('Número de boleta o equivalente.'),
		}
		widgets = {
			'results_private':ToggleWidget(options={ 'on': 'Verdadero', 'off': 'Falso'})
			}

class StudentProfileForm(forms.ModelForm):
	class Meta:
		model = Student
		exclude = ['user']

class TeacherProfileForm(forms.ModelForm):
	class Meta:
		model = Teacher
		exclude = ['user']

class AcademyProfileForm(forms.ModelForm):
	class Meta:
		model = Academy
		fields = ['name']

class SubjectProfileForm(forms.ModelForm):
	class Meta:
		model = Subject
		exclude = ['fields']

