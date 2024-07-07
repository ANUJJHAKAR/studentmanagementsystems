from django.forms import JSONField
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
import pandas as pd
from .models import *
from .decorators import *
from .forms import *
from django.core.files.storage import FileSystemStorage
import json

@login_required(login_url='login')
def home(request):
    if Admin.objects.filter(user=request.user).exists():
        request.session['user_id'] = Admin.objects.get(user=request.user).user_id
        return redirect('admin_home')
    elif Mentor.objects.filter(user=request.user).exists():
        request.session['user_id'] = Mentor.objects.get(user=request.user).user_id
        return redirect('mentor_home')
    elif Student.objects.filter(user=request.user).exists():
        request.session['user_id'] = Student.objects.get(user=request.user).user_id
        return redirect('student_home')
    else:
        messages.error(request, "User role not recognized.")
        return redirect('login')

@login_required(login_url='login')
def admin_home(request):
    if(request.session.get('admin')):
        return render(request, 'admin_home.html',{'obj':Admin.objects.get(user_id=request.session.get('user_id'))})
    elif(request.session.get('mentor')):
        return redirect('mentor_home')
    elif(request.session.get('student')):
        return redirect('student_home')

@login_required(login_url='login')
def mentor_home(request):
    if(request.session.get('mentor')):
        length = Student.objects.filter(mentor=Mentor.objects.get(user=request.user).name).count()
        return render(request, 'mentor_home.html',{'mentor':Mentor.objects.get(user_id=request.session.get('user_id')),'length':length})
    elif(request.session.get('admin')):
        return redirect('admin_home')
    elif(request.session.get('student')):
        return redirect('student_home')

@login_required(login_url='login')
def student_home(request):
    if(request.session.get('student')):
        return render(request, 'student_home.html',{'student':Student.objects.get(user_id=request.session.get('user_id'))})
    elif(request.session.get('admin')):
        return redirect('admin_home')
    elif(request.session.get('mentor')):
        return redirect('mentor_home')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            request.session['student'] = True if user.is_student else False
            request.session['mentor'] = True if user.is_mentor else False
            request.session['admin'] = True if not user.is_student and not user.is_mentor else False
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')

@login_required(login_url='login')
@not_mentor_or_student_required
def createMentor(request):
    if request.method == 'POST':
        form = MentorForm(request.POST)
        if form.is_valid():
            mentor = form.save(commit=False)
            user = CustomUser.objects.create_user(email=mentor.email,password=mentor.email,is_staff=True ,is_mentor=True)
            user.save()
            mentor.user = user
            mentor.save()
            messages.success(request, 'Mentor created successfully.')
            return redirect('admin_home')
    else:
        form = MentorForm()
    return render(request, 'createMentor.html', {'form': form})

@login_required(login_url='login')
@not_mentor_or_student_required
def manageMentors(request):
    if request.method=="POST":
        search_query = request.POST.get('search')
        objs = Mentor.objects.filter(name__icontains=search_query)
        return render(request, 'manageMentors.html', {'objs': objs,'query':True})
    return render(request, 'manageMentors.html',{'objs':None,'query':False})

@login_required(login_url='login')
@not_mentor_or_student_required
def updateMentor(request, id):
    mentor = get_object_or_404(Mentor, user_id=id)
    
    if request.method == 'POST':
        mentor.name = request.POST.get('mentor_name')
        mentor.dob = request.POST.get('mentor_dob')
        mentor.email = request.POST.get('mentor_email')
        mentor.gender = request.POST.get('mentor_gender')
        mentor.mobile = request.POST.get('mentor_mobile')
        mentor.save()
        
        messages.success(request, 'Mentor updated successfully.')
        return redirect('admin_home')
    
    return render(request, 'updateMentor.html', {'mentor': mentor})

@login_required(login_url='login')
@not_mentor_or_student_required
def deleteMentor(request, id):
    mentor = get_object_or_404(Mentor, user_id=id)
    user = mentor.user
    mentor.delete()
    user.delete()
    messages.success(request, 'Mentor deleted successfully.')
    return redirect('admin_home')

@login_required(login_url='login')
@not_mentor_or_student_required
def mentorProfile(request, id):
    mentor = get_object_or_404(Mentor, user_id=id)
    return render(request, 'mentorProfile.html', {'mentor': mentor})

@login_required(login_url='login')
@not_mentor_or_student_required
def createStudent(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        if file.name.endswith('.json'):
            fs = FileSystemStorage(location='media/JSON')
            fname = fs.save(file.name, file)
            data = json.loads(fs.open(fname).read().decode('utf-8'))['data']
            student = Student()
            student.name = data.get('name')
            student.regnum = data.get('regnum')
            student.mobile = data.get('phone')
            try:
                student.dob = datetime.strptime(data.get('dob'), '%Y %m %d').strftime('%Y-%m-%d')
            except:
                student.dob = datetime.strptime(data.get('dob'), '%d %b %Y').strftime('%Y-%m-%d')
            student.email = data.get('email').lower()
            student.address = data.get('address')
            student.gender = data.get('gender')
            student.father_name = data.get('father_name')
            student.father_mobile = data.get('father_mobile')
            student.mother_name = data.get('mother_name')
            student.mother_mobile = data.get('mother_mobile')
            student.branch = data.get('branch')
            student.section = data.get('section')
            student.semester = data.get('semester')
            student.cgpa = data.get('cgpa')
            student.totalCredits = int(float(data.get('totalCreditsEarned')))
            student.grades = data.get('grades')
            user = CustomUser.objects.create_user(email=student.email, password=student.email, is_active=True, is_student=True)
            student.user = user
            student.save()
            user.save()
            messages.success(request, 'Student created successfully.')
            return redirect('admin_home')
        else:
            messages.error(request, 'Please upload a valid JSON file.')
            return redirect('createStudent')
    else:
        return render(request, 'createStudent.html')

@login_required(login_url='login')
@not_mentor_or_student_required
def manageStudents(request):
    if request.method=="POST":
        search_query = request.POST.get('search')
        objs = Student.objects.filter(name__icontains=search_query)
        return render(request, 'manageStudents.html', {'objs': objs,'query':True})
    return render(request, 'manageStudents.html',{'objs':None,'query':False})

@login_required(login_url='login')
@not_mentor_or_student_required
def updateStudent(request, id):
    student = get_object_or_404(Student, user_id=id)
    
    if request.method == 'POST':
        try:
            student.name = request.POST.get('student_name')
            student.regnum = request.POST.get('student_regnum')
            student.mobile = request.POST.get('student_mobile')
            student.dob = request.POST.get('student_dob')
            student.email = request.POST.get('student_email')
            student.address = request.POST.get('student_address')
            student.gender = request.POST.get('student_gender')
            student.father_name = request.POST.get('student_father_name')
            student.father_mobile = request.POST.get('student_father_mobile')
            student.mother_name = request.POST.get('student_mother_name')
            student.mother_mobile = request.POST.get('student_mother_mobile')
            student.branch = request.POST.get('student_branch')
            student.section = request.POST.get('student_section')
            student.semester = request.POST.get('student_semester')
            student.cgpa = request.POST.get('student_cgpa')
            student.totalCredits = request.POST.get('student_total_credits')

            grades = {}
            for key, value in request.POST.items():
                if key.startswith('grades'):
                    parts = key.split('[')
                    if len(parts) == 4:
                        semester = parts[1].strip(']')
                        subject = parts[2].strip(']')
                        field = parts[3].strip(']')
                        
                        if semester not in grades:
                            grades[semester] = {}
                        
                        if subject not in grades[semester]:
                            grades[semester][subject] = {}
                        
                        grades[semester][subject][field] = value
                    elif len(parts) == 3:
                        semester = parts[1].strip(']')
                        field = parts[2].strip(']')
                        grades[semester][field] = value

            formatted_grades = {}
            for semester, details in grades.items():
                formatted_grades[semester] = {}
                for subject, data in details.items():
                    if 'subject' in data and 'grade' in data:
                        formatted_grades[semester][data['subject']] = data['grade']
                    elif subject == 'GPA':
                        formatted_grades[semester]['GPA'] = data
                    elif subject == 'Credits':
                        formatted_grades[semester]['Credits'] = data
            student.grades = formatted_grades
            student.save()
            
            messages.success(request, 'Student updated successfully.')
        except Exception as e:
            messages.error(request, f'Error updating student: {e}')
        return redirect('admin_home')
    
    return render(request, 'updateStudent.html', {'student': student})

@login_required(login_url='login')
@not_mentor_or_student_required
def deleteStudent(request, id):
    student = get_object_or_404(Student, user_id=id)
    user = student.user
    student.delete()
    user.delete()
    messages.success(request, 'Student deleted successfully.')
    return redirect('admin_home')

@login_required(login_url='login')
@not_mentor_or_student_required
def studentProfile(request, id):
    student = get_object_or_404(Student, user_id=id)
    return render(request, 'studentProfile.html', {'student': student})

@login_required(login_url='login')
@not_mentor_or_student_required
def assignMentors(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        if file.name.endswith('.xlsx'):
            fs = FileSystemStorage(location='media/Excel')
            fname = fs.save(file.name, file)
            data = pd.read_excel(fs.path(fname))
            for mentee,mentor in zip(data['Mentee'],data['Mentor']):
                try:
                    student = get_object_or_404(Student, name=mentee)
                    student.mentor = mentor
                    student.save()
                except:
                    pass
            messages.success(request, 'Mentors assigned successfully.')
            return redirect('admin_home')
        else:
            messages.error(request, 'Please upload a valid Excel file.')
            return redirect('assignMentors')
    else:
        return render(request, 'assignMentors.html')

@login_required(login_url='login')
@mentor_required
def menteeList(request):
    mentees = Student.objects.filter(mentor=Mentor.objects.get(user=request.user).name)
    return render(request, 'menteeList.html', {'mentees': mentees})

@login_required(login_url='login')
@mentor_required
def menteeProfile(request, id):
    mentee = get_object_or_404(Student, user_id=id)
    return render(request, 'menteeProfile.html', {'mentee': mentee})

@login_required(login_url='login')
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changePassword.html', {'form': form})


@login_required(login_url='login')
def logout_view(request):
    request.session.pop('admin', None)
    request.session.pop('mentor', None)
    request.session.pop('student', None)
    request.session.pop('user_id', None)
    request.session.flush()
    logout(request)
    return redirect('login')