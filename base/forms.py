from django import forms
from .models import ChatMessage, UploadedFiles, User
from django.contrib.auth.forms import UserCreationForm

class MessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ["context"]
        widgets = {
            'context': forms.Textarea(
                attrs={
                    'placeholder':'Type your question', 
                    'autocomplete':'off',
                    'rows': '1',
                    'contenteditable':'on',
                    }
                )
        }

class FileForm(forms.ModelForm):
    class Meta:
        model = UploadedFiles
        fields = ['uploaded_file']

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role']

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))

