# Generated by Django 4.2.7 on 2024-01-04 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.SET_DEFAULT, to='posts.category'),
        ),
    ]
