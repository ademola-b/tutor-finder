from django.test import TestCase
import uuid
# Create your tests here.
from .models import VerificationStatus

def generate_uuid():
    docs = VerificationStatus.objects.filter(credential__tutor__tutor_id="27390c68-46e8-45db-aaae-f73e831257fe")
    print(docs)


generate_uuid()
