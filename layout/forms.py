from django import forms
from json import loads
from urllib import request

data = None
with request.urlopen("https://jdavidpm.github.io/my-static-files/teamBuilder/json/hexaco_items.json") as url:
	data = loads(url.read().decode(encoding='utf-8'))


class PersonalityTestForm(forms.Form):
	def __init__(self, *args, **kwargs):
		CHOICES_STATEMENT =(("1",  "1"),#"Completamente en Desacuerdo"),
					("2", "2"),#"En Desacuerdo"),
					("3", "3"),#"Neutral"),
					("4", "4"),#"De Acuerdo"),
					("5", "5")#"Completamente de Acuerdo")
					)
		super(PersonalityTestForm, self).__init__(*args, **kwargs)
		for d in data:
			self.fields['statement_%s' % d['statement_id']] = forms.ChoiceField(label= d['statement_text'], choices=CHOICES_STATEMENT, widget=forms.RadioSelect(attrs={"required": "required"}))