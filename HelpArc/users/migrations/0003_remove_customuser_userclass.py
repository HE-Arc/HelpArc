# Generated by Django 2.1.5 on 2019-03-27 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190322_1542'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='userClass',
        ),
    ]
