from celery import current_app
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

User = get_user_model()


@override_settings(
    CELERY_BROKER_URL="memory://",
    CELERY_RESULT_BACKEND="cache+memory://",
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_TASK_EAGER_PROPAGATES=True,
)
class ChatEndpointTests(APITestCase):
    def setUp(self):
        # Ensure the current Celery app uses these settings.
        current_app.conf.update(
            broker_url="memory://",
            result_backend="cache+memory://",
            task_always_eager=True,
            task_eager_propagates=True,
        )
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.client = APIClient()

    def test_authenticated_chat(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("chat_view")
        data = {"message": "Test chat message"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn("task_id", response.data)

    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)
        url = reverse("chat_view")
        data = {"message": "Test chat message"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


if __name__ == "__main__":
    import django

    django.setup()
    ChatEndpointTests().run()
