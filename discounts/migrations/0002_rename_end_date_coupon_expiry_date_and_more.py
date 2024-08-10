# Generated by Django 4.2.15 on 2024-08-10 15:36

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_productimage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupon',
            old_name='end_date',
            new_name='expiry_date',
        ),
        migrations.RemoveField(
            model_name='coupon',
            name='amount',
        ),
        migrations.AddField(
            model_name='coupon',
            name='applicable_products',
            field=models.ManyToManyField(blank=True, related_name='applicable_coupons', to='shop.product'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='coupon_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='coupon',
            name='description',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='coupon',
            name='discount_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='coupon',
            name='excluded_products',
            field=models.ManyToManyField(blank=True, related_name='excluded_coupons', to='shop.product'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='min_purchase_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='coupon',
            name='name',
            field=models.CharField(default=None, max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coupon',
            name='per_user_limit',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='discount_type',
            field=models.CharField(choices=[('percentage', 'Percentage'), ('fixed', 'Fixed Amount'), ('free_shipping', 'Free Shipping')], default='percentage', max_length=20),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='CouponUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('used_at', models.DateTimeField(auto_now_add=True)),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discounts.coupon')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('coupon', 'user')},
            },
        ),
    ]
