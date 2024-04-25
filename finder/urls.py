from django.urls import path
from . views import (DashboardView, BookSessionView, 
                     PendingTutorSession, DeletePendingSession,
        
                     PendingSessionAction, SearchResult, 
                     TerminateSessionView, TerminatedSessionsView)

app_name = 'finder'
urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('book-session/', BookSessionView.as_view(), name='book_session'),
    path('pending-requests/', PendingTutorSession.as_view(), name="pending_session"),
    path('requests/<uuid:pk>/delete/', DeletePendingSession.as_view(), name="delete_session"),
    path('requests/<uuid:pk>/action/', PendingSessionAction.as_view(), name="session_action"),
    path('search-tutor/', SearchResult.as_view(), name="search_tutor"),
    path('terminate-session/<uuid:pk>/', TerminateSessionView.as_view(), name="terminate_session"),
    path('terminated-session/', TerminatedSessionsView.as_view(), name="terminated_sessions"),
]