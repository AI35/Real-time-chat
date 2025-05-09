from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from chat.models import Room, Message, get_timestamp_with_offset
from datetime import timedelta

class RoomModelTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(
            name='Test Room',
            slug='test-room'
        )
    
    def test_room_creation(self):
        self.assertEqual(self.room.name, 'Test Room')
        self.assertEqual(self.room.slug, 'test-room')
    
    def test_room_str_method(self):
        self.assertEqual(str(self.room), 'Test Room')

class MessageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.room = Room.objects.create(
            name='Test Room',
            slug='test-room'
        )
        self.message = Message.objects.create(
            room=self.room,
            user=self.user,
            content='Hello, world!'
        )
    
    def test_message_creation(self):
        self.assertEqual(self.message.content, 'Hello, world!')
        self.assertEqual(self.message.user, self.user)
        self.assertEqual(self.message.room, self.room)
        
    def test_message_str_method(self):
        expected_str = f'{self.user.username}: Hello, world! [{self.message.timestamp}]'
        self.assertEqual(str(self.message), expected_str)
    
    def test_message_ordering(self):
        # Create a second message
        message2 = Message.objects.create(
            room=self.room,
            user=self.user,
            content='Second message'
        )
        
        # Get all messages and check ordering
        messages = Message.objects.all()
        self.assertEqual(messages[0], self.message)
        self.assertEqual(messages[1], message2)
    
    def test_timestamp_offset(self):
        # Test the timestamp offset function
        now = timezone.now()
        offset_time = get_timestamp_with_offset()
        expected_time = now + timedelta(hours=3)
        
        # Allow for a small difference due to execution time
        self.assertLess((offset_time - expected_time).total_seconds(), 1)