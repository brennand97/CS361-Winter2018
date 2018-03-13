# Generated by Django 2.0.2 on 2018-03-13 04:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matchmaking', '0002_auto_20180303_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='dog',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='matchmaking.UserProfile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_shelter',
            field=models.BooleanField(default=False),
        ),
    ]
