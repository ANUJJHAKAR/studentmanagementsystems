# Generated by Django 5.0.6 on 2024-07-02 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_semester_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semester',
            name='sem',
            field=models.CharField(max_length=50),
        ),
    ]
