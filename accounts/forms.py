from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'id': 'exampleInputEmail1','class':'form-control form-control-lg', 'placeholder':'Username', 'autofocus': 'true'}))
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'id':'exampleInputPassword1','class':'form-control form-control-lg', 'placeholder':'Password'}))

class SignUpForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}),
                               )
    email = forms.EmailField(required=True, max_length=254, help_text='Enter a valid email address', widget=forms.EmailInput(attrs={'id': 'email', 'class': 'form-control', 'placeholder':'Email Address'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id': 'password', 'class': 'form-control', 'placeholder':'Enter Password'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id': 'password', 'class': 'form-control', 'placeholder':'Confirm Password'}))
    is_tutor = forms.BooleanField(label='Are you a tutor?', required=False, widget=forms.CheckboxInput(attrs={'required': False}))

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
            'is_tutor'
        ]