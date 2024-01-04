# serializers.py

from rest_framework import serializers
from .models import Note, NoteShare
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class NoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Note
        fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at', 'deleted_at', 'status']
        read_only_fields = ['user']


class NoteShareSerializer(serializers.ModelSerializer):
    note = NoteSerializer(read_only=True)
    shared_with = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = NoteShare
        fields = ['note', 'shared_with']

class SharedNotesSerializer(serializers.ModelSerializer):
    note = NoteSerializer(read_only=True)

    class Meta:
        model = NoteShare
        fields = ['note']


class SharedMembersSerializer(serializers.ModelSerializer):
    shared_with = UserSerializer(read_only= True)

    class Meta:
        model = NoteShare
        fields = ['shared_with']
