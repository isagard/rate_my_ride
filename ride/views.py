from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse 
from ride.forms import ServiceForm
from ride.forms import ReviewForm
from ride.forms import UserForm, UserProfileForm
from ride.models import ServicePage, Review
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from datetime import datetime

def home(request):
    
    visitor_cookie_handler(request)

    response = render(request, 'rango/home.html')
    return response

def glasgow(request):
    service_list = ServicePage.objects.order_by('location')

    city_dict = {}
    city_dict['boldmessage'] = 'This is the Glasgow page'
    city_dict['services'] = service_list
    
    visitor_cookie_handler(request)

    return render(request, 'ride/glasgow.html', context=city_dict)

def edinburgh(request):
    service_list = ServicePage['location'].objects.order_by('-views')

    city_dict = {}
    city_dict['boldmessage'] = 'This is the Edinburgh page'
    city_dict['services'] = service_list
    
    visitor_cookie_handler(request)
    
    return render(request, 'ride/edinburgh.html', context=city_dict)

def aberdeen(request):
    service_list = ServicePage['location'].objects.order_by('-views')

    city_dict = {}
    city_dict['boldmessage'] = 'This is the Aberdeen page'
    city_dict['services'] = service_list
    
    visitor_cookie_handler(request)
    
    return render(request, 'ride/aberdeen.html', context=city_dict)

@login_required
def add_service(request, service_name_slug):
    try:
        service = Service.objects.get(slug=service_name_slug)
    except Service.DoesNotExist:
        service = None

    if service is None:
        return redirect('/ride/')

    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            if service:
                review = form.save(commit=False)
                review.service = service
                review.views = 0
                review.save()

                return redirect(reverse('ride:show_service',kwargs={'service_name_slug':service_name_slug}))
    else:
        print(form.errors)

        context_dict = {'form': form, 'service': service}
        return render(request, 'ride/add_service.html', context=context_dict)

@login_required
def add_review(request):
    form = ServiceForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/ride/')
        else:
            print(form.errors)

    return render(request, 'rango/add_review.html', {'form': form})

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,'ride/register.html',context = {'user_form': user_form,'profile_form': profile_form,'registered': registered})


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('ride:index'))

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits
