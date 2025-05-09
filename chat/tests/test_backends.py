from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from chat.backends import EmailOrUsernameModelBackend

class EmailOrUsernameModelBackendTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.backend = EmailOrUsernameModelBackend()
    
    def test_authenticate_with_username(self):
        user = authenticate(username='testuser', password='testpassword')
        self.assertIsNotNone(user)
        self.assertEqual(user, self.user)
    
    def test_authenticate_with_email(self):
        user = authenticate(username='test@example.com', password='testpassword')
        self.assertIsNotNone(user)
        self.assertEqual(user, self.user)
    
    def test_authenticate_with_wrong_password(self):
        user = authenticate(username='testuser', password='wrongpassword')
        self.assertIsNone(user)
    
    def test_authenticate_with_nonexistent_user(self):
        user = authenticate(username='nonexistentuser', password='testpassword')
        self.assertIsNone(user)
    
    def test_authenticate_case_insensitive_username(self):
        user = authenticate(username='TestUser', password='testpassword')
        self.assertIsNotNone(user)
        self.assertEqual(user, self.user)
    
    def test_authenticate_case_insensitive_email(self):
        user = authenticate(username='Test@Example.com', password='testpassword')
        self.assertIsNotNone(user)
        self.assertEqual(user, self.user)