# Generated by Django 2.0.2 on 2018-03-14 02:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matchmaking', '0003_auto_20180312_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='dog',
            name='has_shelter',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='dog',
            name='shelter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='matchmaking.Shelter'),
        ),
        migrations.AlterField(
            model_name='dog',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='matchmaking.UserProfile'),
        ),
    ]
