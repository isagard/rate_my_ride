from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    context_dict = {'boldmessage': 'This is the homepage'}
    return render(request, 'ride/home.html', context=context_dict)

def glasgow(request):
    context_dict = {'boldmessage': 'This is the Glasgow page'}
    return render(request, 'ride/glasgow.html', context=context_dict)

def edinburgh(request):
    context_dict = {'boldmessage': 'This is the Edinburgh page'}
    return render(request, 'ride/edinburgh.html', context=context_dict)

def aberdeen(request):
    context_dict = {'boldmessage': 'This is the Aberdeen page'}
    return render(request, 'ride/aberdeen.html', context=context_dict)

