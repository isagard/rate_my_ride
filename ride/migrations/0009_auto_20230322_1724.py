# Generated by Django 2.2.28 on 2023-03-22 17:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ride', '0008_auto_20230322_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
