# Generated by Django 2.2.14 on 2021-01-24 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='Item_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
