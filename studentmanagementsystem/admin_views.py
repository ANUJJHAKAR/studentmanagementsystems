from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from app.models import Course, CustomUser, Student
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.EmailBackEnd import EmailBackend

def admin_login(request):
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
            return redirect('admin_home')
        else:
            return redirect('admin_login')
    else:
        return render(request, 'admin_login.html')

@login_required(login_url='admin_login')
def admin_home(request):
    return render(request, 'admin_home.html')

def Add_Students(request):
    global Student
    course = Course.objects.all()

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        mobile_no = request.POST.get('mobile_no')
        address = request.POST.get('address')
        course_id = request.POST.get('course_id')
        semester = request.POST.get('semester')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email already registered.')
            return redirect('Add_Students')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username already registered.')
            return redirect('Add_Students')
        else:
            user = CustomUser(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                user_type = 3

            )
            user.set_password(password)
            user.save()
            course = Course.objects.get(id=course_id)

            student = Student(
                admin=user,
                address=address,
                mobile_no=mobile_no,
                course_id=course,
                semester=semester,
                gender=gender,

            )
            student.save()
            messages.success(request, 'Added Successfully')
            return redirect('Add_Students')

    context = {
        'course': course,

    }
    return render(request, 'Add_Students.html', context)


def Add_Teachers(request):
    return render(request, 'Add_Teachers.html')
