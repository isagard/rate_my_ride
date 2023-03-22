from django.urls import path
from ride import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'ride'

urlpatterns = [
    path('', views.home, name='home'),
    path('glasgow/', views.glasgow, name='glasgow'),
    path('edinburgh/', views.edinburgh, name='edinburgh'),
    path('aberdeen/', views.aberdeen, name='aberdeen'),
    path('<str:location>/add_service/', views.add_service, name='add_service'),
    path('<str:location>/<slug:service_name_slug>/', views.show_services, name='show_services'),
    path('<str:location>/<slug:service_name_slug>/add_review', views.add_review, name='add_review'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('like_review/<int:review_id>/', views.like_review, name='like'),
] 
