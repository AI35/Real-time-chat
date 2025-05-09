from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Email or Username', max_length=254)
    
    error_messages = {
        'invalid_login': 'Please enter a correct email/username and password.',
        'inactive': 'This account is inactive.',
    }