# Generated by Django 5.0.2 on 2024-03-23 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subcategory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
