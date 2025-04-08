from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
import json

class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')  # Assuming you named the url 'home'

    def test_home_view_returns_hello_message(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {"message": "Hello from product catalog!"})