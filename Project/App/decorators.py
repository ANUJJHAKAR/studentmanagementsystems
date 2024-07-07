from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def not_mentor_or_student_required(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and not (request.user.is_mentor or request.user.is_student):
            return function(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrapper

def mentor_required(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_mentor:
            return function(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrapper