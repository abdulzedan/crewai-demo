from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatEndpointTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = APIClient()
    
    def test_authenticated_chat(self):
        # Force authentication for the client (simulating a valid JWT)
        self.client.force_authenticate(user=self.user)
        url = reverse('chat_view')
        data = {"message": "Software Engineer position"}
        response = self.client.post(url, data, format='json')
        # Expecting a 202 ACCEPTED response and a task_id in the output
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn("task_id", response.data)
    
    def test_unauthenticated_access(self):
        # Remove authentication to simulate an unauthenticated request
        self.client.force_authenticate(user=None)
        url = reverse('chat_view')
        data = {"message": "AI job inquiry"}
        response = self.client.post(url, data, format='json')
        # Expecting a 401 Unauthorized response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
