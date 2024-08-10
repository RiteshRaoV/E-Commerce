# Generated by Django 4.2.15 on 2024-08-10 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brands_and_categories', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='brand',
            name='brand_image',
            field=models.ImageField(
                blank=True, null=True, upload_to='brand_logos/'),
        ),
    ]