from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from ..models import Note

class NoteListCreateViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser0', password='testpassword0')
        self.client.force_authenticate(user=self.user)

    def test_note_list_view(self):
        Note.objects.create(user=self.user, title='Test Note 1', content='Content 1')
        Note.objects.create(user=self.user, title='Test Note 2', content='Content 2')

        response = self.client.get('http://127.0.0.1:8000/api/notes/')  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_create_note_view(self):
        data = {'title': 'New Note', 'content': 'New Content'}

        response = self.client.post('http://127.0.0.1:8000/api/notes/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        note = Note.objects.get(title='New Note')
        self.assertEqual(note.content, 'New Content')
        self.assertEqual(note.user, self.user)

