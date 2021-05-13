from django import forms
from users.models import Team

class TeamUpdateForm(forms.ModelForm):
	class Meta:
		model = Team
		fields = ['name', 'projects']

		labels = {
			'name':('Nombre'),
			'projects':('Proyectos'),
			}

class TeamCreateForm(forms.ModelForm):
	class Meta:
		model = Team
		fields = ['founder', 'name', 'projects']
		labels = {
				'founder':('Creador'),
				'name':('Nombre'),
				'projects':('Proyectos')
				}
	def __init__(self, *args, **kwargs): 
		super(TeamCreateForm, self).__init__(*args, **kwargs)                       
		self.fields['founder'].disabled = True

class TeamMembersForm(forms.ModelForm):
	class Meta:
		model = Team
		fields = ['members']
		labels = {'members':('Integrantes')}	