# Generated by Django 5.2.3 on 2025-06-17 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_app_management', '0009_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_type',
            field=models.CharField(choices=[('paid', 'paid'), ('unpaid', 'unpaid')], default=1, max_length=255),
            preserve_default=False,
        ),
    ]
