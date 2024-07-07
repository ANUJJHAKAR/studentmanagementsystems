from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.name

class Mentor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10)
    mobile = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    regnum = models.CharField(max_length=100, unique=True)
    mobile = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    address = models.TextField(max_length=500)
    gender = models.CharField(max_length=10)
    father_name = models.CharField(max_length=100)
    father_mobile = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    mother_mobile = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    semester = models.CharField(max_length=10)
    cgpa = models.FloatField()
    totalCredits = models.IntegerField()
    mentor = models.CharField(max_length=100, null=True, blank=True)
    grades = models.JSONField()

    def __str__(self):
        return self.name
