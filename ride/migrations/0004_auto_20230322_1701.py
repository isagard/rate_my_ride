# Generated by Django 2.2.28 on 2023-03-22 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ride', '0003_servicepage_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ride.UserProfile'),
        ),
    ]
