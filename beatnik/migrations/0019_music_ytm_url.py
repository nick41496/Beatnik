# Generated by Django 2.2.13 on 2021-04-02 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beatnik', '0018_auto_20200125_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='ytm_url',
            field=models.URLField(null=True, unique=True, verbose_name='Youtube Music URL'),
        ),
    ]