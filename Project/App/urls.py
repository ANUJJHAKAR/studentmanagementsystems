from django.urls import path,include
from . import views

adminPatterns = [
    path('', views.admin_home, name='admin_home'),
    path('createMentor', views.createMentor, name='createMentor'),
    path('manageMentors', views.manageMentors, name='manageMentors'),
    path('updateMentor/<int:id>/', views.updateMentor, name='updateMentor'),
    path('deleteMentor/<int:id>/', views.deleteMentor, name='deleteMentor'),
    path('mentorProfile/<int:id>/', views.mentorProfile, name='mentorProfile'),
    path('createStudent', views.createStudent, name='createStudent'),
    path('manageStudents', views.manageStudents, name='manageStudents'),
    path('updateStudent/<int:id>/', views.updateStudent, name='updateStudent'),
    path('deleteStudent/<int:id>/', views.deleteStudent, name='deleteStudent'),
    path('studentProfile/<int:id>/', views.studentProfile, name='studentProfile'),
    path('assignMentors', views.assignMentors, name='assignMentors'),
]

studentPatterns = [
    path('',views.student_home, name='student_home'),
]

mentorPatterns = [
    path('',views.mentor_home, name='mentor_home'),
    path('menteeList', views.menteeList, name='menteeList'),
    path('menteeProfile/<int:id>/', views.menteeProfile, name='menteeProfile'),
]

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_home/',include(adminPatterns)),
    path('mentor_home/',include(mentorPatterns)),
    path('student_home/', include(studentPatterns)),
    path('changePassword', views.changePassword, name='changePassword'),
]
