from django import forms
from users.models import Project, Task, ResourceURL
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

class ResourceURLForm(forms.ModelForm):
	class Meta:
		model = ResourceURL
		fields = ['project', 'name', 'url', 'service']
		labels = {
			'project': ('Proyecto'),
			'name': ('Nombre'),
			'url': ('Enlace'),
			'service': ('Servicio'),
		}
	def __init__(self, *args, **kwargs):
		super(ResourceURLForm, self).__init__(*args, **kwargs)
		self.fields['project'].disabled = True

class DateTimeInput(forms.DateTimeInput):
	input_type = 'datetime-local'

class TaskForm(forms.ModelForm):
	#due_date = forms.DateTimeField(widget=forms.widgets.DateTimeInput(format="%Y-%m-%dT%H:%M"))
	def __init__(self,*args,**kwargs):
		member_choices = kwargs.pop('team_members', None)
		super(TaskForm,self).__init__(*args,**kwargs)
		if member_choices:
			self.fields['assigned_members'] = forms.ModelMultipleChoiceField(
				widget=forms.CheckboxSelectMultiple,
				queryset=member_choices.distinct(),
				label = 'Asignar a'
			)
	#due_date = forms.DateTimeField(input_formats=["%Y-%m-%dT%H:%M"])

	class Meta:
		model = Task
		fields = ['name', 'description', 'due_date', 'status', 'assigned_members']
		labels = {
			'due_date': ('Vencimiento'),
		}
		widgets = {'due_date': DateTimeInput(format = "%Y-%m-%dT%H:%M")}

class NewTaskForm(forms.ModelForm):
	#due_date = forms.DateTimeField(widget=forms.widgets.DateTimeInput(format="%Y-%m-%dT%H:%M"))
	def __init__(self,*args,**kwargs):
		member_choices = kwargs.pop('team_members', None)
		super(NewTaskForm,self).__init__(*args,**kwargs)
		self.fields['author'].disabled = True
		self.fields['project'].disabled = True
		if member_choices:
			self.fields['assigned_members'] = forms.ModelMultipleChoiceField(
				widget=forms.CheckboxSelectMultiple,
				queryset=member_choices.distinct(),
				label = 'Asignar a',
			)
	#due_date = forms.DateTimeField(input_formats=["%Y-%m-%dT%H:%M"])

	class Meta:
		model = Task
		fields = '__all__'
		labels = {
			'due_date': ('Vencimiento'),
		}
		widgets = {'due_date': DateTimeInput(format = "%Y-%m-%dT%H:%M")}