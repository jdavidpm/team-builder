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