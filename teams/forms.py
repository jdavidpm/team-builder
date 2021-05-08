from django import forms
from users.models import Team

class TeamUpdateForm(forms.ModelForm):
	class Meta:
		model = Team
		fields = ['name', 'members', 'projects']

		labels = {
			'name':('Nombre'),
			'members':('Miembros'),
			'projects':('Proyectos'),
			}

class TeamCreateForm(forms.ModelForm):
	class Meta:
		model = Team
		fields = ['founder', 'name', 'members', 'projects']
		labels = {
				'founder':('Creador'),
				'name':('Nombre'),
				'members':('Integrantes'),
				'projects':('Proyectos')
				}
	def __init__(self, *args, **kwargs): 
		super(TeamCreateForm, self).__init__(*args, **kwargs)                       
		self.fields['founder'].disabled = True