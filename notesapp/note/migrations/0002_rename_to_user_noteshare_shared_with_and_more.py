# Generated by Django 4.2.9 on 2024-01-04 07:32

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('note', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='noteshare',
            old_name='to_user',
            new_name='shared_with',
        ),
        migrations.AlterUniqueTogether(
            name='noteshare',
            unique_together={('note', 'shared_with')},
        ),
        migrations.RemoveField(
            model_name='noteshare',
            name='from_user',
        ),
    ]
