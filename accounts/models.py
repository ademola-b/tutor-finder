import datetime
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    class Sex(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
    user_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    middle_name = models.CharField(max_length=150, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic/', default='default.jpg')
    phone = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=7, choices=Sex.choices, default='other')
    address = models.TextField()

    def __str__(self):
        return self.username
    
class Student(models.Model):
    student_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    education_level = models.CharField(max_length=100)
    subject_interest = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
    
class Tutor(models.Model):
    tutor_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    specialized_subject = models.CharField(max_length=100)
    isAvailable = models.BooleanField(default=False)
    isVerified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
class TutorCredential(models.Model):
    class Credential(models.TextChoices):
        ID = "ID", "National ID"
        CERT = "CERT", "Highest Certificate"
        CV = "CV", "Curriculum Vitae"
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    document = models.FileField(upload_to='tutor_credentials/', choices=Credential.choices)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user.username}, Document: {self.document.name}, Uploaded at: {self.uploaded_at}"

class VerificationStatus(models.Model):
    credential = models.OneToOneField(TutorCredential, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verified_by')
    isVerified = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True, null=True)
    verified_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"Tutor Credential: {self.credential}, Verified: {self.isVerified}"






