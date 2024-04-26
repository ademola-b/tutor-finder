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
    email = models.EmailField(unique=True)
    middle_name = models.CharField(max_length=150, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic/', default='default.jpg')
    phone = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=7, choices=Sex.choices, default='other')
    address = models.TextField()
    is_tutor = models.BooleanField(default=False)

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
    specialized_subject = models.CharField(max_length=100, null=True, blank=True)
    qualifications = models.CharField(max_length=300)
    experience_year = models.PositiveIntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    location = models.CharField(max_length=100, help_text="city, state", null=True, blank=True)
    isAvailable = models.BooleanField(default=False)
    isVerified = models.BooleanField(default=False)

    def __str__(self):
        return f"username: {self.user.username}, verification:{self.isVerified}, availablity: {self.isAvailable}"
    
class TutorCredential(models.Model):
    class Credential(models.TextChoices):
        ID = "ID", "National ID"
        CERT = "CERTIFICATE", "Highest Certificate"
        CV = "CV", "Curriculum Vitae"
    tutor_cred_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    document_name = models.CharField(max_length=20, choices=Credential.choices)
    document = models.FileField(upload_to='tutor_credentials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"User: {self.tutor.user.username}, Document: {self.document_name}, Uploaded at: {self.uploaded_at}"

class VerificationStatus(models.Model):
    status_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    credential = models.OneToOneField(TutorCredential, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verified_by', null=True, blank=True)
    isVerified = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True, null=True)
    verified_at = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "Verification Status"

    def __str__(self):
        return f"Tutor Credential: {self.credential}, Verified: {self.isVerified}"






