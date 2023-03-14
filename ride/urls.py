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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
