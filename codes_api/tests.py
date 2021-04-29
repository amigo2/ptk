from rest_framework.test import RequestsClient
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from django.test import TestCase
from codes_api.utils import calculate_distance


# test outcodes api view
class OutcodesTest(APITestCase):

    def test_outcodes(self):
        user = User.objects.create_user(username='test1', password='testpass')
        self.client.login(username=user.username, password='testpass')
        response = self.client.get('http://0.0.0.0:8000/api/outcode/M1')
        self.assertEqual(response.status_code, 200)


 # test nexus api view function
class NexusTest(APITestCase):

    def test_nexus(self):
        user = User.objects.create_user(username='test1', password='testpass')
        self.client.login(username=user.username, password='testpass')
        response = self.client.get('http://0.0.0.0:8000/api/nexus/M1')
        print(response.status_code, status)
        assert response.status_code == 200
        

# test to calculate distance function
class CalculateDistanceTest(TestCase):

    # claculate distance betwen Lyon and Paris
    def test_calculate_distance(self):
        self.assertEqual(calculate_distance(45.7597,4.8422,48.8567,2.3508),392.2172595594006)


