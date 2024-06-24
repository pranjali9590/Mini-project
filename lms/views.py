from django.views.generic import ListView
from django.shortcuts import redirect, render
from app.models import Categories, Course, Level, Video, UserCourse, Payment
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib import messages
from time import time
from .settings import *


from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from app.forms import CourseForm


def base(request):
    return render(request, 'base.html')

def home(request):
    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status = 'PUBLISH').order_by('-id')
    context = {
        'category': category,
        'course': course,
    }
    return render(request, 'main/home.html',context)

def single_course(request):
    category = Categories.get_all_category(Categories)
    level = Level.objects.all()
    course = Course.objects.all()
    FreeCourse_count = Course.objects.filter(price = 0).count()
    PaidCourse_count =  Course.objects.filter(price__gte = 1).count()

    context = {
        'category':category,
        'level':level,
        'course':course,
        'FreeCourse_count':FreeCourse_count,
        'PaidCourse_count':PaidCourse_count,

    }
    return render(request, 'main/single_course.html', context)

def about_us(request):
    category = Categories.get_all_category(Categories)

    context = {
        'category': category
    }
    return render(request, 'main/about_us.html', context)

def contact_us(request):
    category = Categories.get_all_category(Categories)

    context = {
        'category': category
    }
    return render(request, 'main/contact_us.html', context)

def filter_data(request):
    categories = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')
    print(price)


    if price == ['pricefree']:
       course = Course.objects.filter(price=0)
    elif price == ['pricepaid']:
       course = Course.objects.filter(price__gte=1)
    elif price == ['priceall']:
       course = Course.objects.all()
    elif categories:
       course = Course.objects.filter(category__id__in=categories).order_by('-id')
    elif level:
       course = Course.objects.filter(level__id__in = level).order_by('-id')
    else:
       course = Course.objects.all().order_by('-id')


    t = render_to_string('ajax/course.html', {'course': course})

    return JsonResponse({'data': t}) 

def SEARCH_COURSE(request):
    category = Categories.get_all_category(Categories)
       
    query = request.GET['query']
    course = Course.objects.filter(title__icontains = query)
    context = {
        'course':course,
        'category': category
    }

    return render(request,'search/search.html',context)

def COURSE_DETAILS(request, slug):
    category = Categories.get_all_category(Categories)
    time_duration  = Video.objects.filter(course__slug = slug).aggregate(sum=Sum('time_duration'))
    
    course_id = Course.objects.get(slug = slug)

    course = Course.objects.filter(slug = slug)

    try:
        check_enroll = UserCourse.objects.get(user = request.user, course=course_id)
    except UserCourse.DoesNotExist:
        check_enroll = None

    if course.exists():
        course = course.first()

    else:
        return redirect('404')
    
    context = {
        'course': course,
        'category': category,
        'time_duration' : time_duration,
        'check_enroll' : check_enroll,
    }

    return render(request, 'course/course_details.html', context)

def PAGE_NOT_FOUND(request):
    category = Categories.get_all_category(Categories)
    context = {
        'category': category,
    }
    return render(request, 'error/404.html', context)

def CHECKOUT(request, slug):
    course = Course.objects.get(slug = slug)

    if course.price == 0:
        usercourse = UserCourse(user=request.user, course=course)
        usercourse.save()
        messages.success(request, 'Your Course Has Been Successfully Enrolled!')
        return redirect('my_course')
    else:
        context = {'course': course}
        return render(request, 'checkout/checkout.html', context)
        
        
        

def process_payment(request, slug):
    if request.method == "POST":  
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        company = request.POST['company']
        country = request.POST['country']   
        address_1 = request.POST['address_1']  
        address_2 = request.POST['address_2'] 
        city = request.POST['city']
        state = request.POST['state']  
        postcode = request.POST['postcode']  
        phone = request.POST['phone']
        email = request.POST['email']  
        order_comments = request.POST['order_comments']

        course = Course.objects.get(slug=slug)

        # Create UserCourse instance
        user_course = UserCourse(user=request.user, course=course)
        user_course.save()

        # Create Payment instance
        payment = Payment(
            user_course=user_course,
            user=request.user,
            course=course,
            first_name=first_name,
            last_name=last_name,
            company=company,
            country=country,
            address_1=address_1,
            address_2=address_2,
            city=city,
            state=state,
            postcode=postcode,
            phone=phone,
            email=email,
            order_comments=order_comments
        )

        # Save Payment instance
        payment.save()

        # Optional: You may want to do additional actions with the payment instance here

        return redirect('my_course')  # Redirect to the appropriate view after successful payment

    return render(request, 'checkout/checkout.html')
            

def MY_COURSE(request):

    course = UserCourse.objects.filter(user = request.user)

    context = {
        'course':course,
    }
    return render(request, 'course/my-course.html', context)

def WATCH_COURSE(request, slug):

    #course = Course.objects.filter('slug=slug')

    lecture=request.GET.get('lecture')
    
    #course_id = Course.objects.get(slug=slug)
    course = Course.objects.filter(slug=slug)
    video=Video.objects.get(id=lecture)

    #try:
     #   check_enroll = UserCourse.objects.get(user=request.user, course=course_id)
      #  video = Video.objects.get(id=lecture)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')
    #except UserCourse.DoesNotExist:
     #   return redirect('404')
    
    context = {
        'course':course,
        'video':video,
       # 'lecture':lecture,
    }
    return render(request, 'course/watch-course.html', context)


class AddCourseView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'admin/add_course.html'
    success_url = reverse_lazy('add_course_success')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def add_course_success(request):
    return render(request, 'admin/add_course_success.html')

class CourseListView(ListView):
    model = Course
    template_name = 'admin/course_list.html'  # Create this template

    def get_queryset(self):
        return Course.objects.all()
    

