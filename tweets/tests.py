import json

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from tweets.models import Tweet

User = get_user_model()


class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='cde', password='1233454password')
        self.user_2 = User.objects.create(username='cde-2', password='1233454password123')
        Tweet.objects.create(content='my first tweet', user=self.user)
        Tweet.objects.create(content='my second tweet', user=self.user)
        Tweet.objects.create(content='my third tweet', user=self.user_2)
        self.currentCount = Tweet.objects.all().count()

    def test_tweet_created(self):
        tweet = Tweet.objects.create(content='my fourth tweet', user=self.user)
        self.assertEqual(tweet.id, 4)
        self.assertEqual(tweet.user, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username='cde', password='1233454password')
        return client

    def test_tweet_list(self):
        client = self.get_client()
        response = client.get('/api/tweets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_action_like(self):
        client = self.get_client()
        client.force_login(self.user)
        response = client.post("/api/tweets/action/", data={"id": 1, "action": "like"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 1)

    def test_action_unlike(self):
        self.client = self.get_client()
        self.client.force_login(self.user)
        response = self.client.post("/api/tweets/action/", data={"id": 1, "action": "like"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 1)
        response = self.client.post("/api/tweets/action/", data={"id": 1, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 0)

    def test_action_retweet(self):
        data = {"id": 2, "action": "retweet"}
        current_count = self.currentCount
        json_data = json.dumps(data)
        client = self.get_client()
        client.force_login(self.user)
        response = client.post("/api/tweets/action/", data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        data = response.json()
        new_tweet_id = data.get('id')
        self.assertNotEqual(2, new_tweet_id)
        self.assertEqual(current_count + 1, new_tweet_id)

    def test_create_api_view(self):
        data = {'content': 'This is my tweet'}
        client = self.get_client()
        client.force_login(self.user)
        response = client.post("/api/tweets/create/", data)
        self.assertEqual(response.status_code, 201)

    def test_tweet_detail_api_view(self):
        client = self.get_client()
        response = client.get('/api/tweets/1/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get('id')
        self.assertEqual(_id, 1)

    def test_tweet_delete_api_view(self):
        client = self.get_client()
        client.force_login(self.user)
        response = client.delete('/api/tweets/1/delete/')
        self.assertEqual(response.status_code, 200)
        response = client.delete('/api/tweets/1/delete/')
        self.assertEqual(response.status_code, 404)
        response = client.delete('/api/tweets/3/delete/')
        self.assertEqual(response.status_code, 403)

