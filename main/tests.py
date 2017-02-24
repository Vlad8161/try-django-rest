import random

from django.test import Client
from django.test import TestCase
from rest_framework import status


class ProfileTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_self_profile_success(self):
        users = init(self.client)
        user = random.choice(users)
        r = self.client.post('/main/profile', token=user['token'])
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in r.json())
        user['id'] = r.json()['id']
        self.assertJSONEqual(str(r.content, encoding='utf-8'), {
            'username': user['username'],
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'id': user['id'],
            'friends': [],
        })

    def test_get_self_profile_invalid_token(self):
        init(self.client)
        r = self.client.post('/main/profile', token='1234567890987654321')
        self.assertEquals(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_profile_by_id_success(self):
        users = init(self.client)
        user1 = random.choice(users)
        users.remove(user1)
        user2 = random.choice(users)
        r = self.client.post('/main/profile', token=user1['token'])
        user1['id'] = r.json()['id']
        r = self.client.post('/main/profile/' + str(user1['id']), token=user2['token'])
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(str(r.content, encoding='utf-8'), {
            'id': user1['id'],
            'username': user1['username'],
            'email': user1['email'],
            'first_name': user1['first_name'],
            'last_name': user1['last_name'],
            'friends': [],
        })

    def test_get_profile_by_id_not_exist(self):
        users = init(self.client)
        for i in users:
            r = self.client.post('/main/profile', token=i['token'])
            i['id'] = r.json()['id']
        ids = [i['id'] for i in users]
        not_exist_id = random.randint(0, 9999999999)
        while id in ids:
            not_exist_id = random.randint(0, 9999999999)
        r = self.client.post('/main/profile/' + str(not_exist_id), token=random.choice(users)['token'])
        self.assertEquals(r.status_code, status.HTTP_404_NOT_FOUND)


class UpdateProfileTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_update_profile_success(self):
        users = fill_ids(self.client, init(self.client))
        user = random.choice(users)
        r = self.client.post('/main/update-profile', token=user['token'], data={
            'email': user['email'] + '123',
            'first_name': user['first_name'] + '123',
            'last_name': user['last_name'] + '123',
        })
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        r = self.client.post('/main/profile', token=user['token'])
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(str(r.content, encoding='utf-8'), {
            'id': user['id'],
            'username': user['username'],
            'first_name': user['first_name'] + '123',
            'last_name': user['last_name'] + '123',
            'email': user['email'] + '123',
            'friends': [],
        })

    def test_update_profile_failed_not_all_fields_present(self):
        users = fill_ids(self.client, init(self.client))
        user = random.choice(users)
        r = self.client.post('/main/update-profile', token=user['token'], data={
            'email': user['email'] + '123',
            'last_name': user['last_name'] + '123',
        })
        self.assertEquals(r.status_code, status.HTTP_400_BAD_REQUEST)
        r = self.client.post('/main/profile', token=user['token'])
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(str(r.content, encoding='utf-8'), {
            'id': user['id'],
            'username': user['username'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'email': user['email'],
            'friends': [],
        })

    def test_update_profile_success_with_blank_fields(self):
        users = fill_ids(self.client, init(self.client))
        user = random.choice(users)
        r = self.client.post('/main/update-profile', token=user['token'], data={
            'email': '',
            'last_name': '',
            'first_name': '',
        })
        self.assertEquals(r.status_code, status.HTTP_400_BAD_REQUEST)
        r = self.client.post('/main/profile', token=user['token'])
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(str(r.content, encoding='utf-8'), {
            'id': user['id'],
            'username': user['username'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'email': user['email'],
            'friends': [],
        })


class FriendsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_add_friend_success(self):
        users = fill_ids(self.client, init(self.client))
        user = random.choice(users)
        users.remove(user)
        friend = random.choice(users)
        r = self.client.post('/main/add-friend/' + str(friend['id']), token=user['token'])
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        r = self.client.post('/main/profile', token=user['token'])
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(str(r.content, encoding='utf-8'), {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'friends': [
                {
                    'id': friend['id'],
                    'username': friend['username'],
                    'email': friend['email'],
                    'first_name': friend['first_name'],
                    'last_name': friend['last_name'],
                }
            ]
        })

    def test_add_friend_fail_no_such_user(self):
        users = fill_ids(self.client, init(self.client))
        ids = [user['id'] for user in users]
        not_exist_user = random.randint(0, 9999999999)
        while not_exist_user in ids:
            not_exist_user = random.randint(0, 9999999999)
        user = random.choice(users)
        r = self.client.post('/main/add-friend/' + str(not_exist_user), token=user['token'])
        self.assertEquals(r.status_code, status.HTTP_404_NOT_FOUND)
        r = self.client.post('/main/profile', token=user['token'])
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(str(r.content, encoding='utf-8'), {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'friends': [],
        })

    def test_add_friend_fail_friend_is_user(self):
        users = fill_ids(self.client, init(self.client))
        user = random.choice(users)
        r = self.client.post('/main/add-friend/' + str(user['id']), token=user['token'])
        self.assertEquals(r.status_code, status.HTTP_400_BAD_REQUEST)
        r = self.client.post('/main/profile', token=user['token'])
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(str(r.content, encoding='utf-8'), {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'friends': [],
        })

    def test_remove_friend_success(self):
        users = fill_ids(self.client, init(self.client))
        user = random.choice(users)
        users.remove(user)
        friend = random.choice(users)
        self.client.post('/main/add-friend/' + str(friend['id']), token=user['token'])
        r = self.client.post('/main/remove-friend/' + str(friend['id']), token=user['token'])
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        r = self.client.post('/main/profile', token=user['token'])
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(str(r.content, encoding='utf-8'), {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'friends': [],
        })

    def test_remove_friend_success_when_this_user_was_not_friend(self):
        users = fill_ids(self.client, init(self.client))
        user = random.choice(users)
        users.remove(user)
        friend = random.choice(users)
        users.remove(friend)
        friend2 = random.choice(users)
        self.client.post('/main/add-friend/' + str(friend['id']), token=user['token'])
        r = self.client.post('/main/remove-friend/' + str(friend2['id']), token=user['token'])
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        r = self.client.post('/main/profile', token=user['token'])
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(str(r.content, encoding='utf-8'), {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'friends': [
                {
                    'id': friend['id'],
                    'username': friend['username'],
                    'email': friend['email'],
                    'first_name': friend['first_name'],
                    'last_name': friend['last_name'],
                }
            ],
        })

    def test_remove_friend_fail_no_such_user(self):
        users = fill_ids(self.client, init(self.client))
        user = random.choice(users)
        users.remove(user)
        ids = [user['id'] for user in users]
        not_exist_user = random.randint(0, 9999999999)
        while not_exist_user in ids:
            not_exist_user = random.randint(0, 9999999999)
        r = self.client.post('/main/remove-friend/' + str(not_exist_user), token=user['token'])
        self.assertEquals(r.status_code, status.HTTP_404_NOT_FOUND)
        r = self.client.post('/main/profile', token=user['token'])
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(str(r.content, encoding='utf-8'), {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'friends': [],
        })


def init(client):
    users = [
        {
            'username': 'john_doe',
            'password': '1234',
            'password2': '1234',
            'email': 'john_doe@mail.ru',
            'first_name': 'john',
            'last_name': 'doe',
        },
        {
            'username': 'sick_bastard',
            'password': '1234',
            'password2': '1234',
            'email': 'sick_bastard@mail.ru',
            'first_name': 'sick',
            'last_name': 'bastard',
        },
        {
            'username': 'john_smith',
            'password': '1234',
            'password2': '1234',
            'email': 'john_smith@mail.ru',
            'first_name': 'john',
            'last_name': 'smith',
        },
        {
            'username': 'walter_mitty',
            'password': '1234',
            'password2': '1234',
            'email': 'walter_mitty@mail.ru',
            'first_name': 'walter',
            'last_name': 'mitty',
        },
    ]

    for user in users:
        client.post('/account/register', data={
            'username': user['username'],
            'password': user['password'],
            'password2': user['password2'],
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
        })
        r = client.post('/account/obtain-token', {
            'username': user['username'],
            'password': user['password'],
        })
        user['token'] = r.json()['token']

    return users


def fill_ids(client, users):
    for user in users:
        r = client.post('/main/profile', token=user['token'])
        user['id'] = r.json()['id']
    return users
