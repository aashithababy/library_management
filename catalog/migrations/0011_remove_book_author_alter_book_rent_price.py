# Generated by Django 4.2.17 on 2024-12-16 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_yourmodel'),
    ]

    operations = [
        
        migrations.AlterField(
            model_name='book',
            name='rent_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
