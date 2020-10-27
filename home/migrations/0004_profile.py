# Generated by Django 2.0.8 on 2020-08-15 05:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('home', '0003_delete_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user_auth', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('mob', models.CharField(default='', max_length=20)),
                ('link_in', models.CharField(default='', max_length=150)),
                ('github', models.CharField(default='', max_length=150)),
                ('lang', models.CharField(default='', max_length=200)),
            ],
        ),
    ]