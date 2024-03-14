# Generated by Django 5.0.3 on 2024-03-12 08:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(choices=[('Male', 'MALE'), ('Female', 'FEMALE'), ('Other', 'OTHER')], max_length=20)),
                ('phone', models.CharField(max_length=14)),
                ('address', models.CharField(max_length=50)),
                ('profile_picture', models.FileField(blank=True, null=True, upload_to='profile_pictures')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
