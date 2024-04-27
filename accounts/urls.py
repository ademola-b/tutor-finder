from django.urls import path
from . views import (LoginView, RegisterView, logout_request,
                     ProfileUpdateView, TutorFormBView,
                    TutorVerificationView, VerifyTutorView, ProfileView, 
                    UsersList, get_users, UserDetail)

app_name = 'auth'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_request, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('users/', UsersList.as_view(), name="users"),
    path('get-users/', get_users, name="get_users"),
    path('users/<uuid:pk>/detail/', UserDetail.as_view(), name="user_detail"),
    path('update-profile/', ProfileUpdateView.as_view(), name='update_profile'),
    path('tutor-profile/', TutorFormBView.as_view(), name='tutor_profile'),
    path('verify/', TutorVerificationView.as_view(), name='verification'),
    path('verify/<uuid:pk>/', VerifyTutorView.as_view(), name='verify_tutor'),

]