from django.urls import path
from . views import DashboardView

app_name = 'finder'
urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard')

]