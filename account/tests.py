from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from rest_framework import status


class RegisterTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_success_register(self):
        response = self.client.post(r'/account/register', {
            'username': 'john_doe',
            'email': 'john_doe@rambler.ru',
            'password': '1234',
            'password2': '1234',
            'first_name': 'john',
            'last_name': 'doe',
        })
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_already_exists(self):
        self.client.post(r'/account/register', {
            'username': 'john_doe1',
            'email': 'john_doe@rambler.ru',
            'password': '1234',
            'password2': '1234',
            'first_name': 'john',
            'last_name': 'doe',
        })
        response = self.client.post(r'/account/register', {
            'username': 'john_doe1',
            'email': 'john_doe@rambler.ru',
            'password': '1234',
            'password2': '1234',
            'first_name': 'john',
            'last_name': 'doe',
        })
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {
            'username': [
                'User john_doe1 already exists'
            ]
        })

    def test_invalid_email(self):
        response = self.client.post(r'/account/register', {
            'username': 'john_doe2',
            'email': 'not_valid_email',
            'password': '1234',
            'password2': '1234',
            'first_name': 'john',
            'last_name': 'doe',
        })
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {
            'email': [
                'Enter a valid email address.'
            ]
        })

    def test_different_passwords(self):
        response = self.client.post(r'/account/register', {
            'username': 'john_doe2',
            'email': 'not_valid_email',
            'password': '1234',
            'password2': '12345',
            'first_name': 'john',
            'last_name': 'doe',
        })
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {
            'email': [
                'Enter a valid email address.'
            ]
        })

    def test_empty_fields(self):
        response = self.client.post(r'/account/register')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {
            'email': [
                'This field is required.'
            ],
            'first_name': [
                'This field is required.'
            ],
            'last_name': [
                'This field is required.'
            ],
            'password': [
                'This field is required.'
            ],
            'password2': [
                'This field is required.'
            ],
            'username': [
                'This field is required.'
            ],
        })

    def test_only_post_allowed(self):
        response = self.client.get('/account/register')
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete('/account/register')
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put('/account/register')
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.head('/account/register')
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.options('/account/register')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.trace('/account/register')
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class ObtainTokenTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_success_obtain_token(self):
        add_user1(self.client)
        response = self.client.post('/account/obtain-token', {
            'username': 'john_doe',
            'password': '1234',
        })
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        json = response.json()
        self.assertTrue('token' in json)

    def test_fail_obtain_token_no_such_user(self):
        add_user1(self.client)
        response = self.client.post('/account/obtain-token', {
            'username': 'john_doe1',
            'password': '1234',
        })
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {
            'detail': 'No such user',
        })

    def test_fail_obtain_token_invalid_password(self):
        add_user1(self.client)
        response = self.client.post('/account/obtain-token', {
            'username': 'john_doe',
            'password': '12341',
        })
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {
            'detail': 'Invalid password',
        })


class InvalidateTokenTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_invalidate_success(self):
        token = add_user_and_obtain_token(self.client)
        response = self.client.post('/account/invalidate-token', token=token)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_invalidate_fail_unexisting_token(self):
        add_user_and_obtain_token(self.client)
        response = self.client.post('/account/invalidate-token', token='12335512358910235981278')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {
            'detail': 'Invalid token'
        })

    def test_invalidate_fail_no_token(self):
        add_user_and_obtain_token(self.client)
        response = self.client.post('/account/invalidate-token')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {
            'detail': 'No token provided'
        })


def add_user_and_obtain_token(client):
    add_user1(client)
    response = client.post('/account/obtain-token', {
        'username': 'john_doe',
        'password': '1234'
    })
    return response.json()['token']


def add_user1(client):
    client.post('/account/register', {
        'username': 'john_doe',
        'email': 'email@mail.ru',
        'password': '1234',
        'password2': '1234',
        'first_name': 'john',
        'last_name': 'doe',
    })
