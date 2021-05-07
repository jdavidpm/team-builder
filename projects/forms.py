from django import forms
from users.models import Project
from users.widgets import ToggleWidget

class ProjectUpdateForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['name', 'description', 'status', 'fields', 'private']

		labels = {
			'name':('Nombre'),
			'description':('Descripción'),
			'status':('Estado'),
			'fields':('Campos'),
			'private':('Privado'),
			}

		widgets = {
			'private':ToggleWidget(options={ 'on': 'Verdadero', 'off': 'Falso'})
			}

class ProjectCreateForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['author', 'name', 'description', 'status', 'fields', 'private']

		labels = {
			'author':('Autor'),
			'name':('Nombre'),
			'description':('Descripción'),
			'status':('Estado'),
			'fields':('Campos'),
			'private':('Privado')
			}

		widgets = {
			'private':ToggleWidget(options={ 'on': 'Verdadero', 'off': 'Falso'})
			}
	def __init__(self, *args, **kwargs): 
		super(ProjectCreateForm, self).__init__(*args, **kwargs)                       
		self.fields['author'].disabled = True