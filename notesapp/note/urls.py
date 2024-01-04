# urls.py

from django.urls import path
from .views import NoteListCreateView, NoteDetailView, NoteShareView, SharedNotesView,SharedMembersView, SearchNotesAPIView

urlpatterns = [
    path('notes/', NoteListCreateView.as_view(), name='note-list-create'),
    path('notes/<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
    path('notes/<int:pk>/share/', NoteShareView.as_view(), name='note-share'),
    path('shared-notes/', SharedNotesView.as_view(), name='shared-notes'),
    path('shared-members/<int:pk>/', SharedMembersView.as_view(), name='shared-notes'),
    path('search/', SearchNotesAPIView.as_view(), name='search-notes'),
]
