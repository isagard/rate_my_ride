from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from ride.forms import ServiceForm
from ride.forms import ReviewForm
from ride.forms import UserForm, UserProfileForm
from ride.models import ServicePage, Review, User, UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
# from ride.bing_search import run_query
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from ride.models import UserProfile

def home(request):

    response = render(request, 'ride/home.html')
    return response

def glasgow(request):
    service_list = ServicePage.objects.filter(location='Glasgow').order_by('name')

    city_dict = {}
    city_dict['services'] = service_list
    city_dict['location'] = 'glasgow'
    
    visitor_cookie_handler(request)

    return render(request, 'ride/glasgow.html', context=city_dict)

def edinburgh(request):
    service_list = ServicePage.objects.filter(location='Edinburgh').order_by('name')

    city_dict = {}
    city_dict['services'] = service_list
    city_dict['location'] = 'edinburgh'
    
    visitor_cookie_handler(request)
    
    return render(request, 'ride/edinburgh.html', context=city_dict)

def aberdeen(request):
    service_list = ServicePage.objects.filter(location='Aberdeen').order_by('name')

    city_dict = {}
    city_dict['services'] = service_list
    city_dict['location'] = "aberdeen"
    
    visitor_cookie_handler(request)
    
    return render(request, 'ride/aberdeen.html', context=city_dict)

def show_services(request, service_name_slug, location):

    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    account_user = user_profile.accountUser

    context_dict = {}
    context_dict['account_user'] = account_user
    
    try:
        service = ServicePage.objects.get(slug=service_name_slug)
        reviews = Review.objects.filter(service=service)
        context_dict['reviews'] = reviews
        context_dict['service'] = service
        context_dict['location'] = location
        context_dict['service_name_slug'] = service_name_slug
    except ServicePage.DoesNotExist:
        context_dict['service'] = None
        context_dict['reviews'] = None
        context_dict['location'] = location
        
    return render(request, 'ride/service.html', context=context_dict)

@login_required
def add_service(request, location):

    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    account_user = user_profile.accountUser

    if account_user == False:
        form = ServiceForm()
        # context_dict = {}
        # context_dict['location'] = location

        if request.method == 'POST':
            form = ServiceForm(request.POST, request.FILES)

            if form.is_valid():
                form.save(commit=True)
                return redirect('/ride/')
            else:
                print(form.errors)
    else:
        return render(request, 'ride/restricted.html')
    
    return render(request, 'ride/add_service.html', {'form': form, 'location': location})

@login_required
def add_review(request, service_name_slug, location):
    try:
        # serviceName = service_name_slug
        serviceName = ServicePage.objects.get(slug=service_name_slug)
        serviceID = ServicePage.objects.get(slug=service_name_slug)
        userID = User.objects.get(id=request.user.id)

    except ServicePage.DoesNotExist:
        serviceName = None

    if serviceName is None:
        return redirect('/ride/')

    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            if serviceName:
                review = form.save(commit=False)
                review.service = serviceName
                review.userID = userID
                review.serviceID = serviceID
                review.views = 0
                review.save()

                return redirect(reverse('ride:show_services', kwargs={'service_name_slug':service_name_slug, 'location': location}))
    else:
        print(form.errors)

        context_dict = {'form': form, 'service_name_slug': serviceName, 'location': location}
        return render(request, 'ride/add_review.html', context=context_dict)

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

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('ride:home'))
            else:
                return HttpResponse("Your Ride account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'ride/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('ride:home'))

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

@login_required
def restricted(request):
    return render(request, 'ride/restricted.html')

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


def profile(request, username):
    selected_user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=selected_user)

    if request.user == selected_user:
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

            if form.is_valid():
                form.save(commit=True)
                return HttpResponseRedirect(request.path_info)
        else:
            form = UserProfileForm(instance=user_profile)
    else:
        form = None

    context = {
        'selected_user': selected_user,
        'user_profile': user_profile,
        'form': form,
    }

    return render(request, 'ride/profile.html', context)

# def search(request):
#     result_list = []

#     if request.method == 'POST':
#         query = request.POST['query'].strip()

#     if query:
    # Run our Bing function to get the results list
    #     result_list = run_query(query)

    # return render(request, 'ride/search.html', {'result_list': result_list})

# @login_required
# def register_profile(request):
#     form = UserProfileForm()
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES)
#         if form.is_valid():
#             user_profile = form.save(commit=False)
#             user_profile.user = request.user
#             user_profile.save()
#             return redirect(reverse('ride:index'))
#     else:
#         print(form.errors)
#         context_dict = {'form': form, 'errors': form.errors}
#     return render(request, 'ride/profile_registration.html', context_dict)

# def goto_url(request):
#     if request.method == 'GET':
#         review_id = request.GET.get('review_id')
#         try:
#             selected_review = Review.objects.get(id=review_id)
#         except Review.DoesNotExist:
#             return redirect(reverse('ride:home'))
#         selected_review.views = selected_review.views + 1
#         selected_review.save()
#         return redirect(selected_review.url)
    
#     return redirect(reverse('ride:home'))

# class ProfileView(View):
#     def get_user_details(self, username):
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             return None
#         user_profile = UserProfile.objects.get_or_create(user=user)[0]
#         form = UserProfileForm({'website': user_profile.website,
#         'picture': user_profile.picture})
#         return (user, user_profile, form)
    
#     @method_decorator(login_required)
#     def get(self, request, username):
#         try:
#             (user, user_profile, form) = self.get_user_details(username)
#         except TypeError:
#             return redirect(reverse('ride:home'))
#         context_dict = {'user_profile': user_profile,
#             'selected_user': user,
#             'form': form}
#         return render(request, 'ride/profile.html', context_dict)
#     @method_decorator(login_required)
#     def post(self, request, username):
#         try:
#             (user, user_profile, form) = self.get_user_details(username)
#         except TypeError:
#             return redirect(reverse('ride:home'))
#         form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
#         if form.is_valid():
#             form.save(commit=True)
#             return redirect('ride:profile', user.username)
#         else:
#             print(form.errors)

#         context_dict = {'user_profile': user_profile, 'selected_user': user,'form': form}
#         return render(request, 'ride/profile.html', context_dict)

# class ListProfilesView(View):
#     @method_decorator(login_required)
#     def get(self, request):
#         profiles = UserProfile.objects.all()
#         return render(request,'ride/list_profiles.html',{'userprofile_list': profiles})