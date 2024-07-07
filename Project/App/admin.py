from django.contrib import admin
from .models import *

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'is_staff', 'is_mentor', 'is_student']
    list_filter = ['is_active', 'is_staff', 'is_mentor', 'is_student']
    search_fields = ['email']

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'email']
    search_fields = ['name', 'email']

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'email', 'dob']
    search_fields = ['name', 'email']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'email', 'dob', 'regnum', 'branch', 'semester', 'section', 'father_name', 'father_mobile', 'mother_name', 'mother_mobile', 'mentor']
    list_filter = ['branch', 'semester', 'section', 'mentor']
    search_fields = ['name', 'email', 'regnum']