# Generated by Django 4.2.7 on 2023-12-04 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
