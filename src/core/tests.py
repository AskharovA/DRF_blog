from django.test import TestCase
from .models import Post
from django.contrib.auth.models import User
from pytils.translit import slugify
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testUser",
            password="123456Aa",
        )
        self.post = Post.objects.create(
            title="Test Post",
            description="Test Post Description",
            content="Test Post Content",
            image="/test.jpg",
            author=self.user,
        )

    def test_create_post(self):
        self.assertIsInstance(self.post, Post)

    def test_str_representation(self):
        self.assertEquals(str(self.post), "Test Post")

    def test_slugify(self):
        self.assertEquals(self.post.slug, slugify(self.post.title))

    def test_saving_and_retrieving_book(self):
        second_post = Post()
        second_post.title = "First Post"
        second_post.description = 'First Post Description'
        second_post.content = 'First Post Content'
        second_post.image = "/test.jpg"
        second_post.author = self.user
        second_post.save()

        posts = Post.objects.all()
        self.assertEquals(posts.count(), 2)


class URLTest(APITestCase):
    def test_url(self):
        response = self.client.get("http://127.0.0.1:8000/api/posts/")
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_tags_url(self):
        response = self.client.get(reverse("tags"))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_aside_url(self):
        response = self.client.get(reverse("aside_posts"))
        self.assertEquals(response.status_code, status.HTTP_200_OK)


class PostAPITest(APITestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create_user(
            username="TestUserModel",
            password="123456Aa",
        )
        self.test_post = Post.objects.create(
            title="Test Post",
            description="Test Post Description",
            content="Test Post Content",
            author=self.test_user,
        )
        self.url = "http://127.0.0.1:8000/api/posts/"
        self.post_url = f"http://127.0.0.1:8000/api/posts/{self.test_post.slug}/"
        token = self.get_token()
        self.api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def get_token(self):
        url = reverse("token")
        data = {"username": "TestUserModel", "password": "123456Aa"}
        self.api_client = APIClient()
        response = self.api_client.post(url, data)
        return response.data["access"]

    def test_list_posts(self):
        response = self.api_client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["count"], 1)

    def test_post_detail(self):
        response = self.api_client.get(self.post_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["title"], self.test_post.title)
        self.assertEquals(response.data["description"], self.test_post.description)
        self.assertEquals(response.data["content"], self.test_post.content)
        self.assertEquals(response.data["slug"], slugify(self.test_post.title))

    def test_post_create(self):
        test_post = {
            "title": "TestPostTitle",
            "description": "TestPostDescription",
            "content": "TestPostContent",
            "author": self.test_user.username,
            "slug": "TestPostSlug",
            "tags": [
                "tag1",
                "tag2",
                'тег3',
                'тег4',
            ],
        }
        response = self.api_client.post(self.url, test_post)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data["title"], test_post["title"])
        self.assertEquals(response.data["description"], test_post["description"])
        self.assertEquals(response.data["content"], test_post["content"])
        self.assertEquals(response.data["slug"], slugify(test_post["title"]))

    def test_update_post(self):
        data = {
            "title": "UpdatedTestPostTitle"
        }
        response = self.api_client.patch(self.post_url, data, format="json")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(data["title"], response.data["title"])

    def test_delete_post(self):
        response = self.api_client.delete(self.post_url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
