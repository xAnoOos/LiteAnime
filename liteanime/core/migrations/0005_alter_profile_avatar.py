# Generated by Django 5.1.7 on 2025-03-28 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_profile_profile_image_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='default-avatar.jpg', upload_to='static/'),
        ),
    ]
