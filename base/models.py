from django.db import models
from django.core.validators import FileExtensionValidator
from .validator import validate_csv_only
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    UserRole = {
        "U": "User",
        "A" :"Admin"
        }
    email = models.EmailField(unique=True, null=True)
    role = models.CharField(max_length=10, choices=UserRole)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    summary = models.TextField(blank=True, default="No summary yet....")
    generated = models.DateField(auto_now=True)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return self.summary

class ChatMessage(models.Model):
    ROLE_CHOICES = {
        "U": "User",
        "M": "Model",
    }
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, null=True, blank=True)
    context = models.TextField(blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)
    created = models.DateField(auto_now=True)

    def __str__(self):
        words = self.context.split()
        if(len(words) > 5):
            return str(f"{self.role}: {' '.join(words[:5])}")
        return str(f"{self.role}: {' '.join(words)}")

class UploadedFiles(models.Model):
    associatedCont = models.ForeignKey(ChatMessage, on_delete = models.CASCADE, null = True, blank = True)
    uploaded_file = models.FileField(
        upload_to='files/', 
        blank=True,
        validators=[validate_csv_only])
    uploaded_at = models.DateTimeField(auto_now_add=True)


