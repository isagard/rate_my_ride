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


class RideSessionPersistenceTests(TestCase):
    """
    Tests to see if session data is persisted by counting up the number of accesses, and examining last time since access.
    """
    def test_visits_counter(self):
        """
        Tests the visits counter.
        Artificially tweaks the last_visit variable to force a counter increment.
        """
        for i in range(0, 10):
            response = self.client.get(reverse('rango:index'))
            session = self.client.session

            self.assertIsNotNone(session['visits'])
            self.assertIsNotNone(session['last_visit'])

            # Get the last visit, and subtract one day.
            # Forces an increment of the counter.
            last_visit = datetime.now() - timedelta(days=1)

            session['last_visit'] = str(last_visit)
            session.save()

            self.assertEquals(session['visits'], i+1)

class RideViewTests(TestCase):
    """
    The index and about views.
    """
    def test_home_view(self):
        """
        Checks that the index view doesn't contain any presentational logic for showing the number of visits.
        """
        response = self.client.get(reverse('ride:index'))
        content = response.content.decode()

        self.assertTrue('visits:' not in content.lower(), f"{FAILURE_HEADER}The home.html template should not contain any logic for displaying the number of views. Did you complete the exercises?{FAILURE_FOOTER}")
        
    def test_visits_passed_via_context(self):
        """
        Checks that the context dictionary contains the correct values.
        """
        response = self.client.get(reverse('ride:home'))  # Set the counter!
        self.assertNotIn('visits', response.context, f"{FAILURE_HEADER}The 'visits' variable appeared in the context dictionary passed by home().{FAILURE_FOOTER}")

        response = self.client.get(reverse('ride:glasgow'))
        self.assertIn('visits', response.context, f"{FAILURE_HEADER}We couldn't find the 'visits' variable in the context dictionary for glasgow(). Check your glasgow() implementation.{FAILURE_FOOTER}")

        response = self.client.get(reverse('ride:edinburgh'))
        self.assertIn('visits', response.context, f"{FAILURE_HEADER}We couldn't find the 'visits' variable in the context dictionary for edinburgh(). Check your edinburgh() implementation.{FAILURE_FOOTER}")

        response = self.client.get(reverse('ride:aberdeen'))
        self.assertIn('visits', response.context, f"{FAILURE_HEADER}We couldn't find the 'visits' variable in the context dictionary for aberdeen(). Check your aberdeen() implementation.{FAILURE_FOOTER}")

class ServicePageTest(TestCase):

    def setUp(self):
        ServicePage.objects.create(name='Test Service', location='Test Location', body='Test Body')

    def test_servicepage_slug_field(self):
        service = ServicePage.objects.get(name='Test Service')
        self.assertEqual(service.slug, 'test-service', f"{FAILURE_HEADER}Test service page failed.{FAILURE_FOOTER}")

class ReviewTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='Test User')
        service = ServicePage.objects.create(name='Test Service', location='Test Location', body='Test Body')
        Review.objects.create(serviceID=service, userID=user, location='Test Location', service='Test Service',
                              rating=5, title='Test Title', body='Test Body')

    def test_review_likes_field(self):
        review = Review.objects.get(title='Test Title')
        user = User.objects.create(username='Test User 2')
        review.likes.add(user)
        self.assertEqual(review.likes.count(), 1, f"{FAILURE_HEADER}Test review likes failed.{FAILURE_FOOTER}")

class UserProfileTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='Test User')
        UserProfile.objects.create(user=user, accountUser=True)

    def test_userprofile_picture_field(self):
        user_profile = UserProfile.objects.get(user__username='Test User')
        self.assertEqual(user_profile.picture.url, '/media/', f"{FAILURE_HEADER}Test user profile picture failed.{FAILURE_FOOTER}")
