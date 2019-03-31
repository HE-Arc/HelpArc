# Generated by Django 2.1.5 on 2019-03-27 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_customuser_userclass'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='titleId',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='picture',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to='profile_pics'),
        ),
    ]
