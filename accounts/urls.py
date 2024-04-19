from django.urls import path
from . views import LoginView, RegisterView, ProfileUpdateView, TutorVerificationView

app_name = 'auth'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('update-profile/', ProfileUpdateView.as_view(), name='update_profile'),
    path('verify/', TutorVerificationView.as_view(), name='verification'),

]