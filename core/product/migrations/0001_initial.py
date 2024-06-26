# Generated by Django 5.0.2 on 2024-03-20 04:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subcategory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(upload_to='product/')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subcategory.subcategory')),
            ],
            options={
                'db_table': 'product',
            },
        ),
    ]
