from django.test import TestCase
from django.contrib.auth.models import User
from chat.forms import RoomForm, SignUpForm, EmailOrUsernameAuthenticationForm
from chat.models import Room

class RoomFormTest(TestCase):
    def test_valid_room_form(self):
        form_data = {'name': 'Test Room'}
        form = RoomForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_empty_room_form(self):
        form_data = {'name': ''}
        form = RoomForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

class SignUpFormTest(TestCase):
    def setUp(self):
        # Create a user for testing email uniqueness
        self.existing_user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='testpassword'
        )
    
    def test_valid_signup_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'complex_password123',
            'password2': 'complex_password123'
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_email_uniqueness(self):
        form_data = {
            'username': 'newuser',
            'email': 'existing@example.com',  # Already exists
            'password1': 'complex_password123',
            'password2': 'complex_password123'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('already in use', form.errors['email'][0])
    
    def test_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'complex_password123',
            'password2': 'different_password123'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_email_required(self):
        form_data = {
            'username': 'testuser',
            'email': '',
            'password1': 'complex_password123',
            'password2': 'complex_password123'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

class EmailOrUsernameAuthenticationFormTest(TestCase):
    def test_form_field_labels(self):
        form = EmailOrUsernameAuthenticationForm()
        self.assertEqual(form.fields['username'].label, 'Email or Username')
        self.assertEqual(form.fields['username'].max_length, 150)