from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from app.models import Student

@login_required(login_url='slogin')
def student_home(request):
    user = request.user
    return render(request, 'student_home.html', {'student': Student})
