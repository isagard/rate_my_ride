# 
# Rate_My_Ride Tests
# 
# To run these tests, make sure this module to your rate_my_ride/ride/ directory.
# Once this is complete, run $ python manage.py test ride.tests_ride
# 
#

import os
import re
import ride.models
from ride import forms
from populate_ride import populate
from datetime import datetime, timedelta
from django.db import models
from django.test import TestCase
from django.conf import settings
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.forms import fields as django_fields
from .models import ServicePage, Review, UserProfile

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

f"{FAILURE_HEADER} {FAILURE_FOOTER}"


class RideConfigurationTests(TestCase):
    """
    Tests the configuration of the Django project -- can cookies be used, at least on the server-side?
    """
    def test_middleware_present(self):
        """
        Tests to see if the SessionMiddleware is present in the project configuration.
        """
        self.assertTrue('django.contrib.sessions.middleware.SessionMiddleware' in settings.MIDDLEWARE)
    
    def test_session_app_present(self):
        """
        Tests to see if the sessions app is present.
        """
        self.assertTrue('django.contrib.sessions' in settings.INSTALLED_APPS)

class RideViewTests(TestCase):
    """
    The index and about views.
    """
    def test_home_view(self):
        """
        Checks that the index view doesn't contain any presentational logic for showing the number of visits.
        """
        response = self.client.get(reverse('ride:home'))
        content = response.content.decode()

        self.assertTrue('visits:' not in content.lower(), f"{FAILURE_HEADER}The home.html template should not contain any logic for displaying the number of views. Did you complete the exercises?{FAILURE_FOOTER}")
        
class UserProfileTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='Test User')
        UserProfile.objects.create(user=user, accountUser=True)

class ReviewsTests(TestCase):
    def test_ensure_views(self):
        user1 = User.objects.create_user(username='user001', email='user001@example.com', password='password')
        review = Review(serviceID='Uber', user_instance=user1.id, location='glasgow', service='Uber', rating='4', title='test title', body='test body', likes =3)
        self.assertEqual(review.__str__(), review.title)

class ServiceTests(TestCase):
    def test_ensure_views(self):
        """
        Ensures the number of views received for a Category are positive or zero.
        """
        service = ServicePage(name='test', location='glasgow', body='this is a test', views=1)
        service.save()
        self.assertEqual((service.location >= 'Glasgow'), True)

    def test_views_counter(self):
        views = uber_glasgow.views
        response = self.client.get(reverse('ride:home:glasgow:uber'))
        session = self.client.session
        self.assertEqual(views, uber_glasgow.views)

    def test_service_name(self):
        
        service = ServicePage(name='test', location='glasgow', body='this is a test', views=1)
        service.save()
        
        self.assertEqual(service.__str__(),service.name)

    def setUp(self):
        ServicePage.objects.create(name='Test Service', location='Test Location', body='Test Body')

    def test_servicepage_slug_field(self):
        service = ServicePage.objects.get(name='Test Service')
        self.assertEqual(service.slug, 'test-service_test-location', f"{FAILURE_HEADER}Test service page failed.{FAILURE_FOOTER}")
