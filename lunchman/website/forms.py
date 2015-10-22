
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from website.models import BEHAVIOUR_CHOICES


###     LoginForm
####################################################################################################

class LoginForm(AuthenticationForm):

    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'username',
        })
    )

    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'placeholder': 'password',
        })
    )


###     UserSettingsForm
####################################################################################################

class UserSettingsForm(forms.Form):

    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
        }),
        required=False,
    )

    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
        }),
        required=False,
    )

    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
        }),
        required=False,
    )

    email = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
        }),
        required=False,
    )

    default_behaviour = forms.ChoiceField(
        # max_length=15,
        widget=forms.RadioSelect(attrs={
            'class': 'radio',
            'type': 'radio',
            'name': 'behaviour-radio',
        }),
        choices=BEHAVIOUR_CHOICES,
    )
