# tests/test_views.py

from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

@override_settings(
    CELERY_BROKER_URL="memory://",
    CELERY_RESULT_BACKEND="cache+memory://",
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_TASK_EAGER_PROPAGATES=True,
)
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


@override_settings(
    CELERY_BROKER_URL="memory://",
    CELERY_RESULT_BACKEND="cache+memory://",
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_TASK_EAGER_PROPAGATES=True,
)
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
