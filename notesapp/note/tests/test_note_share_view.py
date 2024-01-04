from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.test import TestCase
from ..models import Note, NoteShare

class NoteShareViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser0', password='testpassword0')
        self.client.force_authenticate(user=self.user)
        self.note = Note.objects.create(user=self.user, title='Test Note', content='Test Content')

    def test_share_note_with_users(self):
        shared_user1 = User.objects.create_user(username='shareduser1', password='shareduser1password')
        shared_user2 = User.objects.create_user(username='shareduser2', password='shareduser2password')

        data = {'shared_with': ['shareduser1', 'shareduser2']}
        response = self.client.post(f'http://127.0.0.1:8000/api/notes/{self.note.id}/share/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(NoteShare.objects.filter(note=self.note, shared_with=shared_user1).count(), 1)
        self.assertEqual(NoteShare.objects.filter(note=self.note, shared_with=shared_user2).count(), 1)

        self.assertEqual(response.data['message'], 'Note shared successfully')

    def test_share_note_with_nonexistent_user(self):
        data = {'shared_with': ['nonexistentuser']}
        response = self.client.post(f'http://127.0.0.1:8000/api/notes/{self.note.id}/share/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(NoteShare.objects.filter(note=self.note).count(), 0)

