# Generated by Django 2.1.5 on 2019-03-22 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HelpArcApp', '0002_auto_20190322_1542'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='titleId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='HelpArcApp.Title'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='userClass',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='HelpArcApp.Class'),
        ),
    ]