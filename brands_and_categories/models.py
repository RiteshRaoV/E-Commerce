from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Brand(models.Model):
    name = models.CharField(max_length=50)
    brand_image = models.ImageField(
        upload_to='brand_logos/', blank=True, null=True)

    def __str__(self) -> str:
        return self.name
