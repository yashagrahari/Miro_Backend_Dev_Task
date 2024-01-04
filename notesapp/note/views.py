from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Note, NoteShare
from django.contrib.auth.models import User
from .serializers import NoteSerializer, NoteShareSerializer, SharedMembersSerializer, SharedNotesSerializer, UserSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication


class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        # Only include active notes (exclude soft-deleted notes)
        return Note.objects.exclude(deleted_at__isnull=False).filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        instance.soft_delete()
        response_data = {'message': 'Note deleted successfully'}

        return Response(response_data, status=status.HTTP_200_OK)

class NoteShareView(generics.CreateAPIView):
    queryset = NoteShare.objects.all()
    serializer_class = NoteShareSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        note_id = self.kwargs['pk']
        note = generics.get_object_or_404(Note, pk=note_id, user=self.request.user)
        shared_with_usernames = self.request.data.get('shared_with', [])
        
        for username in shared_with_usernames:
            shared_user = User.objects.get(username=username)
            NoteShare.objects.create(note=note, shared_with=shared_user)


class SharedNotesView(generics.ListAPIView):
    serializer_class = SharedNotesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return NoteShare.objects.exclude(note__deleted_at__isnull=False).filter(shared_with=self.request.user).select_related('note')
    

class SharedMembersView(generics.ListAPIView):
    serializer_class = SharedMembersSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        note_id = self.kwargs.get('pk')
        return NoteShare.objects.filter(note_id=note_id).select_related('shared_with')
