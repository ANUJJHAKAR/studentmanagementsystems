from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER = (
        (1, 'admin'),
        (2, 'mentor'),
        (3, 'student'),
    )
    user_type = models.CharField(choices=USER, max_length=50, default=1)


class Course(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    mobile_no = models.IntegerField()
    address = models.CharField(max_length=50)
    semester = models.IntegerField()
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name
