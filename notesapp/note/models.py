from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Note(models.Model):
    STATUS_CHOICES = (
        ('Active', 'ACTIVE'),
        ('Trashed', 'TRASHED'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.status = 'TRASHED'
        self.save()

class NoteShare(models.Model):
    shared_with = models.ForeignKey(User, related_name='received_notes', on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['note', 'shared_with']
