import uuid
from django.contrib.auth import get_user_model
from django.db import models
from accounts.models import Student, Tutor

# Create your models here.
class SessionBook(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    subject = models.CharField(max_length=20)
    date_booked = models.DateTimeField(auto_now_add=True)
    additional_note = models.TextField(default="Hi")
    duration = models.CharField(help_text="10days", max_length=20, null=True, blank=True)
    status = models.CharField(max_length=15, default="pending", choices=[
        ('pending', 'pending'),
        ('ongoing', 'ongoing'),
        ('rejected', 'rejected'),
        ('ended', 'ended'),
        ('terminated', 'terminated')
    ])
    terminator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    termination_reason = models.TextField(default="idk")

    class Meta:
        verbose_name_plural = "Booked Sessions"

    def __str__(self):
        return f"{self.student.user.username}-{self.tutor.user.username}({self.status})"
