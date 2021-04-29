import json
from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.test import Client
from codes_api.utils import calculate_distance
from rest_framework.test import RequestsClient
from rest_framework.test import APITestCase
from django.test import TestCase



class AccountTest(APITestCase, URLPatternsTestCase):
    
    urlpatterns = [
        path('registration/', include('rest_auth.registration.urls')),
        path('api/login/', include('rest_auth.urls')),
    ]


    #Test case create a new user
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        self.client = Client()
        self.user = User(username="testuser", email="testemail@test.com")
        self.user.is_staff = True
        self.user.set_password('secret')
        self.user.save()


    #Test case for a Login case    
    def test_login(self):
        """
        Ensure user can login.
        """
        user = User.objects.create_user(username='test1', password='testpass')
        self.client.login(username=user.username, password='testpass')




