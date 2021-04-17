from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .widgets import ToggleWidget, PictureWidget

class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(label=u'Correo Electrónico')

    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']        

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email']
        labels = {
            'first_name': ('Nombre(s)'),
            'last_name': ('Apellidos'),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        image = forms.ImageField()
        fields = ['school_register', 'experience', 'interests', 'languages', 'frameworks', 'distributions', 'image']
        widgets = {
            'image': forms.widgets.FileInput
        }
        labels = {
            'school_register': ('Matrícula'),
            'experience': ('Experiencia'),
            'interests': ('Intereses'),
            'languages': ('Lenguajes de Programación'),
            'frameworks': ('Frameworks'),
            'distributions': ('Distros'),
            'image': ('Foto de Perfil')
        }
        help_texts = {
            'school_register': ('Número de boleta o equivalente.'),
        }

class JustAnotherForm(forms.Form): #Toggle Widget in use example
    working = forms.BooleanField(
        # required must be false, otherwise you will get error when the toggle is off
        # at least in chrome
        required=False,
        widget=ToggleWidget(
            options={
                'on': 'Yep',
                'off': 'Nope'
            }
        ),
        label=u'Prueba'
    )
