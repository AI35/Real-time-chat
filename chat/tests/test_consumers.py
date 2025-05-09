from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from django.test import TestCase
from django.contrib.auth.models import User
from chat.consumers import ChatConsumer
from chat.models import Room, Message
import json

class ChatConsumerTest(TestCase):
    async def test_connect(self):
        # Create a room
        room = await database_sync_to_async(Room.objects.create)(
            name='Test Room',
            slug='test-room'
        )
        
        # Create a communicator
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(),
            "/ws/chat/test-room/"
        )
        communicator.scope["url_route"] = {"kwargs": {"room_name": "test-room"}}
        
        # Connect
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        
        # Disconnect
        await communicator.disconnect()
    
    async def test_receive_and_broadcast(self):
        # Create a user and room
        user = await database_sync_to_async(User.objects.create_user)(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        room = await database_sync_to_async(Room.objects.create)(
            name='Test Room',
            slug='test-room'
        )
        
        # Create two communicators
        communicator1 = WebsocketCommunicator(
            ChatConsumer.as_asgi(),
            "/ws/chat/test-room/"
        )
        communicator1.scope["url_route"] = {"kwargs": {"room_name": "test-room"}}
        
        communicator2 = WebsocketCommunicator(
            ChatConsumer.as_asgi(),
            "/ws/chat/test-room/"
        )
        communicator2.scope["url_route"] = {"kwargs": {"room_name": "test-room"}}
        
        # Connect both
        connected1, _ = await communicator1.connect()
        connected2, _ = await communicator2.connect()
        self.assertTrue(connected1)
        self.assertTrue(connected2)
        
        # Send a message from communicator1
        message_data = {
            'message': 'Hello, world!',
            'username': 'testuser',
            'room': 'test-room'
        }
        await communicator1.send_json_to(message_data)
        
        # Receive the message on both communicators (broadcast)
        response1 = await communicator1.receive_json_from()
        response2 = await communicator2.receive_json_from()
        
        # Check the responses
        self.assertEqual(response1['message'], 'Hello, world!')
        self.assertEqual(response1['username'], 'testuser')
        self.assertEqual(response1['room'], 'test-room')
        
        self.assertEqual(response2['message'], 'Hello, world!')
        self.assertEqual(response2['username'], 'testuser')
        self.assertEqual(response2['room'], 'test-room')
        
        # Check that the message was saved to the database
        message_count = await database_sync_to_async(Message.objects.filter(
            content='Hello, world!',
            user=user,
            room=room
        ).count)()
        self.assertEqual(message_count, 1)
        
        # Disconnect both
        await communicator1.disconnect()
        await communicator2.disconnect()