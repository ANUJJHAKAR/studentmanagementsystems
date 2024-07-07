# Generated by Django 5.0.6 on 2024-06-30 08:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_course_semester'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('mobileNumber', models.IntegerField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.course')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.semester')),
            ],
        ),
    ]
