from django import forms
from json import load

data = None
with open("static/json/hexaco_items.json", "r", encoding='utf-8') as read_file:
	data = load(read_file)


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
			self.fields['statement_%s' % d['statement_id']] = forms.ChoiceField(label= d['statement_id'] + ' - ' + d['statement_text'], choices=CHOICES_STATEMENT, widget=forms.RadioSelect)