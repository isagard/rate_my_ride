from django.shortcuts import render

@login_required
def add_service_page(request, service_name_slug):
    try:
        service = Service.objects.get(slug=service_name_slug)
    except Service.DoesNotExist:
        service = None

    if service is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if service:
                page = form.save(commit=False)
                page.service = service
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category',kwargs={'category_name_slug':category_name_slug}))
    else:
        print(form.errors)

        context_dict = {'form': form, 'category': category}
        return render(request, 'rango/add_page.html', context=context_dict)

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