from django import forms
from users.models import Chat, ChatMessage, Message, Team, Project
from django.contrib.auth.models import User
from json import loads
from urllib import request
from users.widgets import ToggleWidget
from django.db.models import Q

class TeamCreateForm(forms.ModelForm):
	class Meta:
		model = Team
		fields = ['founder', 'name', 'projects', 'description', 'image','private']
		widgets = {
			'private':ToggleWidget(options={ 'on': 'Verdadero', 'off': 'Falso'})
			}
		labels = {
				'founder':('Creador'),
				'name':('Nombre'),
				'description':('Descripción'),
				'image':('Fondo'),
				'projects':('Proyectos')
				}
	def __init__(self, *args, **kwargs): 
		super(TeamCreateForm, self).__init__(*args, **kwargs)                       
		self.fields['founder'].disabled = True
		self.fields['image'].required = False

class TeamUpdateForm(forms.ModelForm):
	class Meta:
		model = Team
		fields = ['name', 'projects', 'description', 'image', 'private']

		widgets = {
			'private':ToggleWidget(options={ 'on': 'Verdadero', 'off': 'Falso'})
			}

		labels = {
			'name':('Nombre'),
			'projects':('Proyectos'),
			'description':('Descripción'),
			'image':('Fondo'),
			'private':('Privado')
			}
	def __init__ (self, *args, **kwargs):
		current_user = kwargs.pop('current_user')
		super(TeamUpdateForm, self).__init__(*args, **kwargs)
		self.fields["projects"].queryset = Project.objects.filter(author=current_user).distinct()

class TeamMembersForm(forms.ModelForm):
	class Meta:
		model = Team
		fields = ['members']
		labels = {'members':('Integrantes')}
	def __init__ (self, *args, **kwargs):
		current_user = kwargs.pop('current_user')
		query = Q()
		for membership in current_user.membership_teams.all():
			query = query | Q(membership_teams=membership)
		super(TeamMembersForm, self).__init__(*args, **kwargs)
		self.fields["members"].queryset = User.objects.filter(query).distinct()


data = None
with request.urlopen("https://raw.githubusercontent.com/jdavidpm/team-builder/master/static/json/team_performance.json") as url:
	data = loads(url.read().decode(encoding='utf-8'))


class TeamEvaluationForm(forms.Form):
	def __init__(self, *args, **kwargs):
		CHOICES_STATEMENT =(("0",  "0"),#"Completamente en Desacuerdo"),
					("1", "1"),#"En Desacuerdo"),
					("2", "2"),#"Neutral"),
					("3", "3"),#"De Acuerdo"),
					("4", "4")#"Completamente de Acuerdo")
					)
		super(TeamEvaluationForm, self).__init__(*args, **kwargs)
		for d in data:
			self.fields['statement_%s' % d['statement_id']] = forms.ChoiceField(label= d['statement_text'], choices=CHOICES_STATEMENT, widget=forms.RadioSelect)


class NewMessageForm(forms.ModelForm):
	def __init__(self,*args,**kwargs):
		super(NewMessageForm,self).__init__(*args,**kwargs)
		self.fields['from_user'].disabled = True
		self.fields['to_user'].disabled = True
		self.fields['read'].disabled = True
		self.fields['new'].disabled = True
		self.fields['date'].disabled = True
		
	class Meta:
		model = Message
		fields = '__all__'


class NewChatMessageForm(forms.ModelForm):
	def __init__(self,*args,**kwargs):
		super(NewChatMessageForm,self).__init__(*args,**kwargs)
		self.fields['from_user'].disabled = True
		self.fields['chat'].disabled = True
		
	class Meta:
		model = ChatMessage
		fields = '__all__'


class NewChatForm(forms.ModelForm):
		
	class Meta:
		model = Chat
		fields = '__all__'
		labels = {'team':('Selecciona el equipo')}