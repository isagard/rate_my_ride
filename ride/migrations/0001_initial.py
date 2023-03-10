# Generated by Django 2.2.28 on 2023-03-14 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ServicePage',
            fields=[
                ('serviceID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
                ('location', models.CharField(max_length=32)),
                ('body', models.CharField(max_length=256)),
                ('logo', models.ImageField(blank=True, upload_to='logo_images')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website', models.URLField(blank=True)),
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('reviewID', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('location', models.CharField(max_length=32)),
                ('service', models.CharField(max_length=32)),
                ('rating', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=128)),
                ('body', models.CharField(max_length=256)),
                ('serviceID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ride.ServicePage')),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
