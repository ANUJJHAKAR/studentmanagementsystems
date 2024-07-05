from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.EmailBackEnd import EmailBackend
from django.contrib.auth import login
from app.models import Student

def mentor_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = EmailBackend.authenticate(
                request,
                email=request.POST.get('email'),
                password=request.POST.get('password'), 
            )
        if user is not None:
            login(request, user)
            return redirect('mentor_home')
        else:
            return redirect('mentor_login')
    else:
        return render(request, 'mentor_login.html')


@login_required(login_url='mentor_login')
def mentor_home(request):
    return render(request, 'mentor_home.html')