# Generated by Django 2.1.5 on 2019-03-27 18:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HelpArcApp', '0003_auto_20190327_1906'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0007_auto_20190327_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(default='default.png', upload_to='profile_pics')),
                ('accountLevel', models.IntegerField()),
                ('asked_helper', models.BooleanField(default=False)),
                ('is_complete', models.BooleanField(default=False)),
                ('classId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='HelpArcApp.Class')),
                ('titleId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='HelpArcApp.Title')),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='titleId',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='user',
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]