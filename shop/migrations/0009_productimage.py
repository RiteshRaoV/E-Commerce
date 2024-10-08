# Generated by Django 4.2.15 on 2024-08-10 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_rename_image_product_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('product_image', models.ImageField(
                    blank=True, null=True, upload_to='product_images/')),
                ('product', models.ForeignKey(
                    default=None, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.product')),
            ],
        ),
    ]
