# Generated by Django 2.1.5 on 2019-03-22 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('HelpArcApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='requestId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='HelpArcApp.Request'),
        ),
        migrations.AddField(
            model_name='message',
            name='senderId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.CustomUser'),
        ),
        migrations.AddField(
            model_name='request',
            name='helperId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='helper', to='users.CustomUser'),
        ),
        migrations.AddField(
            model_name='request',
            name='studentId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student', to='users.CustomUser'),
        ),
        migrations.AddField(
            model_name='request',
            name='technologyId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='HelpArcApp.Technology'),
        ),
        migrations.AddField(
            model_name='skilllevels',
            name='technologyId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='HelpArcApp.Technology'),
        ),
    ]
