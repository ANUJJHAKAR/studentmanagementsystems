# Generated by Django 5.0.6 on 2024-07-06 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='mentor',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
