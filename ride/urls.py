from django.urls import path
from ride import views

app_name = 'ride'

urlpatterns = [
    path('', views.home, name='home'),
    path('glasgow/', views.glasgow, name='glasgow'),
    path('edinburgh/', views.edinburgh, name='edinburgh'),
    path('aberdeen/', views.aberdeen, name='aberdeen'),
    path('service/<slug:service_name_slug>/', views.show_service,
         name='show_service'),
    path('add_service/', views.add_service, name='add_service'),
]
