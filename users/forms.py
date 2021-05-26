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
		fields = ['school_register', 'school_role', 'description', 'distributions', 'experience', 'interests', 'languages', 'frameworks', 'sw_tools', 'hw_tools', 'results_private', 'image']
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
			'description': ('Acerca de mi'),
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
		fields = ['user', 'entry_year', 'entry_semester', 'career']
		labels = {
			'user': ('Usuario'),
			'entry_year': ('Año de Ingreso'),
			'entry_semester': ('Semestre de Ingreso'),
			'career': ('Carrera'),
		}
	def __init__(self, *args, **kwargs): 
		super(StudentProfileForm, self).__init__(*args, **kwargs)
		self.fields['user'].disabled = True

class TeacherProfileForm(forms.ModelForm):
	class Meta:
		model = Teacher
		fields = ['user', 'entry_year', 'entry_semester', 'academy']
		labels = {
			'user': ('Usuario'),
			'entry_year': ('Año de Ingreso'),
			'entry_semester': ('Semestre de Ingreso'),
			'academy': ('Academia'),
		}
	def __init__(self, *args, **kwargs): 
		super(TeacherProfileForm, self).__init__(*args, **kwargs)
		self.fields['user'].disabled = True

class StudentUpdateForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = ['entry_year', 'entry_semester', 'career']
		labels = {
			'entry_year': ('Año de Ingreso'),
			'entry_semester': ('Semestre de Ingreso'),
			'career': ('Carrera'),
		}

class TeacherUpdateForm(forms.ModelForm):
	class Meta:
		model = Teacher
		fields = ['entry_year', 'entry_semester', 'academy']
		labels = {
			'entry_year': ('Año de Ingreso'),
			'entry_semester': ('Semestre de Ingreso'),
			'academy': ('Academia'),
		}

class AcademyProfileForm(forms.ModelForm):
	class Meta:
		model = Academy
		fields = ['name']

class SubjectProfileForm(forms.ModelForm):
	class Meta:
		model = Subject
		exclude = ['fields']

