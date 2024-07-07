from django.shortcuts import render, redirect, HttpResponse

from django.contrib.auth import authenticate, login, logout

from app.EmailBackEnd import EmailBackend

from django.contrib import messages

def BASE(request):
    return render(request, 'base.html')

def slogin(request):
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
            return redirect('student_home')
        else:
            return redirect('slogin')
    else:
        return render(request, 'slogin.html')

def Logout(request):
    logout(request)
    return redirect('base')

