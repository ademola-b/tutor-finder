from django.urls import path
from . views import DashboardView, BookSessionView

app_name = 'finder'
urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('book-session/', BookSessionView.as_view(), name='book_session')

]