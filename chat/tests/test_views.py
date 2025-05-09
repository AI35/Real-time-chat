from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from chat.models import Room, Message
from django.utils.text import slugify

class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.room = Room.objects.create(name='Test Room', slug='test-room')
    
    def test_index_view(self):
        response = self.client.get(reverse('chat:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/index.html')
        self.assertContains(response, 'Test Room')
        self.assertIn('rooms', response.context)
        self.assertEqual(len(response.context['rooms']), 1)

class RoomViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.room = Room.objects.create(name='Test Room', slug='test-room')
        self.message = Message.objects.create(
            room=self.room,
            user=self.user,
            content='Test message'
        )
    
    def test_room_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('chat:room', args=['test-room']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/room.html')
        self.assertContains(response, 'Test Room')
        self.assertIn('messages', response.context)
        self.assertEqual(len(response.context['messages']), 1)
    
    def test_room_view_unauthenticated(self):
        response = self.client.get(reverse('chat:room', args=['test-room']))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

class SignupViewTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_signup_view_get(self):
        response = self.client.get(reverse('chat:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/signup.html')
    
    def test_signup_view_post_valid(self):
        user_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'complex_password123',
            'password2': 'complex_password123'
        }
        response = self.client.post(reverse('chat:signup'), user_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful signup
        self.assertRedirects(response, reverse('chat:index'))
        
        # Check that the user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # Check that the user is logged in
        user = User.objects.get(username='newuser')
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
    
    def test_signup_view_post_invalid(self):
        user_data = {
            'username': 'newuser',
            'email': 'invalid-email',  # Invalid email
            'password1': 'complex_password123',
            'password2': 'complex_password123'
        }
        response = self.client.post(reverse('chat:signup'), user_data)
        self.assertEqual(response.status_code, 200)  # Stay on the same page
        self.assertTemplateUsed(response, 'chat/signup.html')
        self.assertFalse(User.objects.filter(username='newuser').exists())

class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
    
    def test_logout_view(self):
        response = self.client.get(reverse('chat:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        self.assertRedirects(response, reverse('chat:index'))
        
        # Check that the user is logged out
        user_id = self.client.session.get('_auth_user_id')
        self.assertIsNone(user_id)

class CreateRoomViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a regular user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        # Create a staff user
        self.staff_user = User.objects.create_user(
            username='staffuser',
            email='staff@example.com',
            password='testpassword',
            is_staff=True
        )
    
    def test_create_room_view_staff_get(self):
        self.client.login(username='staffuser', password='testpassword')
        response = self.client.get(reverse('chat:create_room'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/create_room.html')
    
    def test_create_room_view_staff_post_valid(self):
        self.client.login(username='staffuser', password='testpassword')
        room_data = {'name': 'New Room'}
        response = self.client.post(reverse('chat:create_room'), room_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertRedirects(response, reverse('chat:index'))
        
        # Check that the room was created
        self.assertTrue(Room.objects.filter(name='New Room').exists())
        room = Room.objects.get(name='New Room')
        self.assertEqual(room.slug, slugify('New Room'))
    
    def test_create_room_view_non_staff(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('chat:create_room'))
        # Should redirect to login page or show permission denied
        self.assertNotEqual(response.status_code, 200)