import os
from dotenv import load_dotenv

# Ensure the .env file is loaded (assumes it's in the project root)
load_dotenv()

# In case the .env isn’t loaded properly during tests, explicitly set the key:
os.environ.setdefault("AZURE_OPENAI_API_KEY", "9f16cc35170841e593c799f5595ef351")

# Force Celery tasks to run synchronously (bypassing broker connection) for testing.
from django.conf import settings
settings.CELERY_TASK_ALWAYS_EAGER = True

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatEndpointTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = APIClient()
    
    def test_authenticated_chat(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('chat_view')
        data = {"message": "Test chat message"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn("task_id", response.data)
    
    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)
        url = reverse('chat_view')
        data = {"message": "Test chat message"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class AnalysisEndpointTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='analysisuser', password='testpass123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_analysis(self):
        url = reverse('analysis_view')
        data = {
            "document_text": "This is a sample document to analyze. It contains multiple insights and details.",
            "image_url": "https://www.planetware.com/wpimages/2019/11/canada-in-pictures-beautiful-places-to-photograph-morraine-lake.jpg",
            "web_query": "latest trends in AI"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("report", response.data)
