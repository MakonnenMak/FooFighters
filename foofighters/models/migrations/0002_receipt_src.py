# Generated by Django 2.1.1 on 2019-03-03 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='src',
            field=models.TextField(default=''),
        ),
    ]
