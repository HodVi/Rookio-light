from django.test import TestCase, Client, RequestFactory
from .factories import RoomFactory, TagFactory, UserFactory, MenuItemFactory
from django.urls import reverse


class RegisterViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.username = 'testuser'
        self.password = 'password'
        self.user = UserFactory.build()

    def test_registration_success(self):
        # here client simulates a dummy web client that can be used to make requests, without the need of running server
        response = self.client.post(reverse('register'), {
            'username': self.user.username,
            'first_name': 'Janko',
            'last_name': 'Marienkowitch',
            'email': 'JandM@gmail.com',
            'password1': '!letputheresomepass090',
            'password2': '!letputheresomepass090',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Registration successful', response.content.decode())

    def test_registration_failed_mail_format(self):
        response = self.client.post(reverse('register'), {
            'username': self.user.username,
            'first_name': 'Janko',
            'last_name': 'Marienkowitch',
            'email': 'JandM@@.com',
            'password1': '!letputheresomepass090',
            'password2': '!letputheresomepass090',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Enter a valid email address.', response.content.decode())

    def test_registration_failed_common_password(self):
        response = self.client.post(reverse('register'), {
            'username': self.user.username,
            'first_name': 'Janko',
            'last_name': 'Marienkowitch',
            'email': 'JandM@gmail.com',
            'password1': 'asdasd',
            'password2': 'asdasd',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('This password is too common.', response.content.decode())

    def test_login_success(self):
        password = 'testpassword123'
        user = UserFactory(password=password)
        response = self.client.post(reverse('login'), {
            'username': user.username,
            'password': password
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful login
        self.assertIn(response.url, '/')

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'invaliduser',
            'password': 'invalidpassword'
        })
        self.assertEqual(response.status_code, 200)  # Returns to the same page with an error
        self.assertIn('Invalid username or password', response.content.decode())

    def test_login_no_data(self):
        response = self.client.post(reverse('login'), {})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid username or password', response.content.decode())

    def test_welcome(self):
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to Rookio!', response.content.decode())


class RoomActionsTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.username = 'testuser'
        self.password = 'password'
        self.user = UserFactory.create()

    def test_add_room_success(self):
        self.client.force_login(self.user)
        tag = TagFactory()  # Create a sample tag
        data = {
            'name': 'Sample Room',
            'room_type': 'event',
            'description': 'Sample Description',
            'place': 'Sample Place',
            'gps_description': 'Sample GPS Description',
            'date': '2025-12-12',
            'time': '12:00',
            'contact_public': 'Sample@contact.com +999 888 777 444',
            'tag-0': tag.name
        }
        response = self.client.post(reverse('add_room'), data)
        self.assertEqual(response.status_code, 302)
        self.assertIn('my_rooms', response.url)

    def test_add_room_duplicate_tags(self):
        self.client.force_login(self.user)
        data = {
            'name': 'Sample Room',
            'room_type': 'event',
            'description': 'Sample Description',
            'place': 'Sample Place',
            'gps_description': 'Sample GPS Description',
            'date': '2025-12-12',
            'time': '12:00',
            'tag-0': 'DuplicateTag',
            'tag-1': 'DuplicateTag'
        }
        response = self.client.post(reverse('add_room'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Tag names must be unique', response.content.decode())

    def test_add_room_empty_tags(self):
        self.client.force_login(self.user)
        tag = TagFactory()
        data = {
            'name': 'Sample Room',
            'room_type': 'event',
            'description': 'Sample Description',
            'place': 'Sample Place',
            'gps_description': 'Sample GPS Description',
            'date': '2025-12-12',
            'time': '12:00',
            'tag-0': tag.name,
            'tag-1': ''
        }
        response = self.client.post(reverse('add_room'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Tags: This field is required.', response.content.decode())

    def test_my_rooms_no_data(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('my_rooms'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('you have not yet created any room', response.content.decode())

    # def test_rooms_overview(self):
    #     room1 = RoomFactory()
    #     room2 = RoomFactory()
    #     response = self.client.get(reverse('rooms_overview'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(room1.name, response.content.decode())
    #     self.assertIn(room2.name, response.content.decode())

    def test_room_detail_with_items(self):
        room = RoomFactory()
        item1 = MenuItemFactory(room=room)
        item2 = MenuItemFactory(room=room)
        response = self.client.get(reverse('room_detail_with_items', args=[room.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(room.name, response.content.decode())
        self.assertIn(item1.item_name, response.content.decode())
        self.assertIn(item2.item_name, response.content.decode())
