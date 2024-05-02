from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# User Registration Form for sign-up
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Email is required
    mobile = forms.CharField(max_length=15, required=True)  # Mobile field is required

    class Meta:
        model = User
        fields = ['username', 'email', 'mobile', 'password1', 'password2']


# User Login Form for authentication
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)  # Username for login
    password = forms.CharField(widget=forms.PasswordInput())  # Password for login
