# Generated by Django 5.0.6 on 2024-07-31 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_delete_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(default='user', max_length=50),
        ),
    ]