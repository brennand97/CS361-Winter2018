# Generated by Django 2.0.2 on 2018-03-14 03:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matchmaking', '0004_auto_20180313_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='matchmaking.UserProfile'),
        ),
        migrations.AlterField(
            model_name='dog',
            name='shelter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='matchmaking.Shelter'),
        ),
    ]
