# Generated by Django 5.0.6 on 2024-07-31 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_profile_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='created',
        ),
        migrations.RemoveField(
            model_name='product',
            name='updated',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.IntegerField(default=0),
        ),
    ]