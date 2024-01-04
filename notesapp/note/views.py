from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .pagination import CustomPageNumberPagination
from .models import Note, NoteShare
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from .serializers import NoteSerializer, NoteShareSerializer, SharedMembersSerializer, SharedNotesSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache
from django.conf import settings



class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        # Only include active notes (exclude soft-deleted notes)
        user=self.request.user
        user_notes = Note.objects.filter(Q(user=user) & Q(deleted_at__isnull=True)).order_by('-created_at')
        shared_notes = Note.objects.filter(noteshare__shared_with=user, deleted_at__isnull=True).order_by('-created_at')
        all_notes = user_notes | shared_notes
        return all_notes
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        instance.soft_delete()
        response_data = {'message': 'Note deleted successfully'}

        return Response(response_data, status=status.HTTP_200_OK)

class NoteShareView(generics.CreateAPIView):
    queryset = NoteShare.objects.all()
    serializer_class = NoteShareSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        note_id = self.kwargs['pk']
        note = generics.get_object_or_404(Note, pk=note_id, user=self.request.user)
        shared_with_usernames = self.request.data.get('shared_with', [])
        
        for username in shared_with_usernames:
            shared_user = User.objects.get(username=username)
            NoteShare.objects.create(note=note, shared_with=shared_user)

        response_data = {'message': 'Note shared successfully'}
        return Response(response_data, status=status.HTTP_201_CREATED)


class SharedNotesView(generics.ListAPIView):
    serializer_class = SharedNotesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return NoteShare.objects.exclude(note__deleted_at__isnull=False).filter(shared_with=self.request.user).select_related('note')
    

class SharedMembersView(generics.ListAPIView):
    serializer_class = SharedMembersSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        note_id = self.kwargs.get('pk')
        return NoteShare.objects.filter(note_id=note_id).select_related('shared_with')

class SearchNotesAPIView(generics.ListAPIView):
    serializer_class = NoteSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        query = self.request.query_params.get('q', '')

        # Check if the result is already in the cache
        cache_key = f"search_notes:{user.id}:{query}"
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result

        user_notes = Note.objects.filter(Q(user=user) & Q(deleted_at__isnull=True)).order_by('-created_at')
        shared_notes = Note.objects.filter(noteshare__shared_with=user, deleted_at__isnull=True).order_by('-created_at')

        if query:
            user_notes = user_notes.annotate(
                search=SearchVector('title', 'content')
            ).filter(Q(search=query))

            shared_notes = shared_notes.annotate(
                search=SearchVector('title', 'content')
            ).filter(Q(search=query))

        all_notes = user_notes | shared_notes

        # Cache the result for future use
        cache.set(cache_key, all_notes, settings.CACHES['default'].get('TIMEOUT', 300))  # set a timeout (in seconds)

        return all_notes
