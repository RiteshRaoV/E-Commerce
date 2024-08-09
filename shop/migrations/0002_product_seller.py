# Generated by Django 5.0.8 on 2024-08-06 15:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='products', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
