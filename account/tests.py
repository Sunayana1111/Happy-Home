from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from .serializers.user import UserSerializer


class UserRegisterViewTestCase(APITestCase):
    def test_user_register_view(self):
        url = reverse('user_register')
        # Data to be sent in the request
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())


class UserViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_user_view_set_retrieve(self):
        url = reverse('user-detail', kwargs={'username': self.user.username})  # Assuming 'user-detail' is the URL name for UserViewSet

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        serialized_data = UserSerializer(instance=self.user).data
        self.assertEqual(response.data, serialized_data)

    def test_user_view_set_update(self):
        url = reverse('user-detail', kwargs={'username': self.user.username})
        updated_data = {'email': 'updated@example.com'}

        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, updated_data['email'])
