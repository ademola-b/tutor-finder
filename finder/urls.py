from django.urls import path
from . views import (DashboardView, BookSessionView, 
                     PendingTutorSession, DeletePendingSession,
                     PendingSessionAction, SearchResult)

app_name = 'finder'
urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('book-session/', BookSessionView.as_view(), name='book_session'),
    path('pending-requests/', PendingTutorSession.as_view(), name="pending_session"),
    path('requests/<uuid:pk>/delete/', DeletePendingSession.as_view(), name="delete_session"),
    path('requests/<uuid:pk>/action/', PendingSessionAction.as_view(), name="session_action"),
    path('search-tutor/', SearchResult.as_view(), name="search_tutor")
]