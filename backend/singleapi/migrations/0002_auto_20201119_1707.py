# Generated by Django 2.2 on 2020-11-19 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('singleapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='columntypedict',
            options={'ordering': ['pk']},
        ),
        migrations.RemoveField(
            model_name='optiondict',
            name='column_type',
        ),
    ]