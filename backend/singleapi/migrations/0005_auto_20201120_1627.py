# Generated by Django 2.2 on 2020-11-20 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('singleapi', '0004_auto_20201120_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optiondict',
            name='widget',
            field=models.CharField(choices=[('checkbox', '复选框'), ('input', '输入框'), ('select', '下拉框'), ('doubleinput', '区间输入框'), ('null', '无需控件')], default=('输入框', 'input'), max_length=100),
        ),
    ]