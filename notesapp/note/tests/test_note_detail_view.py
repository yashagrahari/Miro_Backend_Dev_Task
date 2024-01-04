from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.test import TestCase
from ..models import Note  

class NoteDetailViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser0', password='testpassword0')
        self.client.force_authenticate(user=self.user)
        self.note = Note.objects.create(user=self.user, title='Test Note', content='Test Content')

    def test_get_note_detail(self):
        response = self.client.get(f'http://127.0.0.1:8000/api/notes/{self.note.id}/') 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Note')
        self.assertEqual(response.data['content'], 'Test Content')

    def test_update_note_detail(self):
        updated_data = {'title': 'Updated Note', 'content': 'Updated Content'}
        response = self.client.put(f'http://127.0.0.1:8000/api/notes/{self.note.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Note')
        self.assertEqual(self.note.content, 'Updated Content')

    def test_soft_delete_note(self):
        response = self.client.delete(f'http://127.0.0.1:8000/api/notes/{self.note.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note.refresh_from_db()
        self.assertIsNotNone(self.note.deleted_at)
        self.assertEqual(response.data['message'], 'Note deleted successfully')

