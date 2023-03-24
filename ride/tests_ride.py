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
from ride.models import ServicePage, Review, UserProfile
from ride.forms import ReviewForm, ServiceForm

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

    def test_home_view(self):
        
        response = self.client.get(reverse('ride:home'))
        content = response.content.decode()

        self.assertTrue('visits:' not in content.lower(), f"{FAILURE_HEADER}The home.html template should not contain any logic for displaying the number of views. Did you complete the exercises?{FAILURE_FOOTER}")
        
class UserProfileTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='Test User')
        UserProfile.objects.create(user=user, accountUser=True)


class ServiceTests(TestCase):
    def test_ensure_views(self):
        """
        Ensures the number of views received for a Category are positive or zero.
        """
        service = ServicePage(name='test', location='glasgow', body='this is a test', views=1)
        service.save()
        self.assertEqual((service.location >= 'Glasgow'), True)



    def setUp(self):
        ServicePage.objects.create(name='Test Service', location='Test Location', body='Test Body')

class ModelsTests(TestCase):
    def test_module_exists(self):
        
        project_path = os.getcwd()
        ride_app_path = os.path.join(project_path, 'ride')
        forms_module_path = os.path.join(ride_app_path, 'forms.py')

        self.assertTrue(os.path.exists(forms_module_path), f"{FAILURE_HEADER}We couldn't find Rango's new forms.py module. This is required to be created at the top of Section 7.2. This module should be storing your two form classes.{FAILURE_FOOTER}")

    def test_service_page_slug(self):
        
        service = ServicePage(name='test', location='glasgow')
        service.save()
        self.assertEqual(service.slug, 'test_glasgow')

    def test_service_name(self):
        
        service = ServicePage(name='test', location='glasgow', body='this is a test', views=1)
        service.save()
        
        self.assertEqual(service.__str__(),service.name)

class FormsTest(TestCase):

    def test_valid_review_form(self):
        form_data = {
            'title': 'Great taxi service!',
            'rating': '5',
            'location': 'glasgow',
            'body': 'I had a fantastic experience with this taxi service. The driver was courteous and prompt, and the car was clean and comfortable.',
            'service': 'glasgo',
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_review_form(self):
        form_data = {
            'title': '',
            'rating': '3',
            'location': '',
            'body': '',
            'service': '',
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_service_form(self):
        """
        Test that an invalid form raises validation errors.
        """
        data = {
            'name': '',
            'location': '',
            'body': '',
            'logo': None,
            'slug': ''
        }
        form = ServiceForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)
        self.assertIn('name', form.errors)
        self.assertIn('location', form.errors)
        self.assertIn('body', form.errors)
        self.assertIn('logo', form.errors)