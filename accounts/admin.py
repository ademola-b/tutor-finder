from django.contrib import admin
from . models import *

# Register your models here.
models = [User, Student, Tutor, TutorCredential, VerificationStatus]

for model in models:
    admin.site.register(model)
    