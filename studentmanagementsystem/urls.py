from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views, admin_views, mentor_views, student_views
urlpatterns = [
                path('base', views.BASE, name='base'),

                path('logout',views.Logout,name = 'logout'),

                #login path
                path('admin_login', admin_views.admin_login, name='admin_login'),
                path('mentor_login', mentor_views.mentor_login, name='mentor_login'),
                path('slogin', views.slogin, name='slogin'),

                #this is for admin
                path('admin_home', admin_views.admin_home, name='admin_home'),
                path('Add_Students', admin_views.Add_Students, name='Add_Students'),
                path('Add_Teachers', admin_views.Add_Teachers, name='Add_Teachers'),


                #this is for mentor
                path('mentor_home', mentor_views.mentor_home, name='mentor_home'),

                #this is for student
                path('student_home', student_views.student_home, name='student_home'),
                
                path('admin', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
