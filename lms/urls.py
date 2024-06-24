from .views import AddCourseView
from django.contrib import admin
from django.urls import path, include
from .import views, user_login
from django.conf import settings
from django.conf.urls.static import static 
from .views import CourseListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base',views.base, name='base'),
    path('courses',views.single_course, name='single_course'),
    path('courses/filter-data',views.filter_data,name="filter-data"),
    path('course/<slug:slug>',views.COURSE_DETAILS, name='course_details'),
    path('404',views.PAGE_NOT_FOUND, name='404'),

    path('about_us',views.about_us, name='about_us'),
    path('contact_us',views.contact_us, name='contact_us'),
    
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', user_login.register, name='register'),
    path('dologin', user_login.dologin, name='dologin'),
    path('accounts/profile', user_login.profile, name='profile'),
    path('accounts/profile_update', user_login.profile_update, name='profile_update'),
    path('search',views.SEARCH_COURSE,name='search_course'),

    path('checkout/<slug:slug>', views.CHECKOUT, name='checkout'),
    path('course/watch-course/<slug:slug>', views.WATCH_COURSE, name='watch_course'),
    path('my-course', views.MY_COURSE, name='my_course'),
    path('process_payment/<slug:slug>/', views.process_payment, name='process_payment'),

    path('add/', AddCourseView.as_view(), name='add_course'),
    path('add/success/', views.add_course_success, name='add_course_success'),
    path('courses/', CourseListView.as_view(), name='course_list'),

    path('', views.home, name='home'),



    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
