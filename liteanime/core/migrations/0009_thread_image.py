# Generated by Django 5.1.7 on 2025-03-28 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='thread_images/'),
        ),
    ]
