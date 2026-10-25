
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Author, Category, Book, Review

User = get_user_model()


class BookAuthorFilterTest(APITestCase):

    def setUp(self):
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")

        self.category = Category.objects.create(name="Programming")

        self.book1 = Book.objects.create(
            title="Python Basics",
            category=self.category,
        )
        self.book1.author.add(self.author1)

        self.book2 = Book.objects.create(
            title="Django Guide",
            category=self.category,
        )
        self.book2.author.add(self.author1)

        self.book3 = Book.objects.create(
            title="Data Science",
            category=self.category,
        )
        self.book3.author.add(self.author2)

    def test_filter_books_by_author_id(self):
        url = reverse("book_filter")

        response = self.client.get(
            url,
            {"author": self.author1.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        returned_ids = {
            book["id"] for book in response.data["results"]
        }

        self.assertEqual(
            returned_ids,
            {self.book1.id, self.book2.id},
        )

    def test_filter_books_by_nonexistent_author_id(self):
        url = reverse("book_filter")

        response = self.client.get(
            url,
            {"author": 99999},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], [])


class ImportantAPITests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            password="TestPassword123!",
        )
        self.user2 = User.objects.create_user(
            username="user2",
            password="TestPassword123!",
        )

        self.author = Author.objects.create(name="Test Author")
        self.category = Category.objects.create(name="Test Category")

        self.book = Book.objects.create(
            title="Test Book",
            category=self.category,
        )
        self.book.author.add(self.author)

    def test_unauthenticated_user_cannot_add_book(self):
        url = reverse("book_create")

        response = self.client.post(
            url,
            {
                "title": "New Book",
                "category": self.category.id,
                "author": [self.author.id],
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_user_cannot_update_another_users_review(self):
        review = Review.objects.create(
            book=self.book,
            user=self.user1,
            rating=3,
            comment="Original comment",
        )

        self.client.force_authenticate(user=self.user2)

        response = self.client.patch(
            reverse("review_update", args=[review.id]),
            {"comment": "Changed by another user"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        review.refresh_from_db()
        self.assertEqual(review.comment, "Original comment")

    def test_user_cannot_delete_another_users_review(self):
        review = Review.objects.create(
            book=self.book,
            user=self.user1,
            rating=4,
            comment="Keep this review",
        )

        self.client.force_authenticate(user=self.user2)

        response = self.client.delete(
            reverse("review_delete", args=[review.id]),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertTrue(
            Review.objects.filter(id=review.id).exists()
        )

    def test_user_cannot_review_same_book_twice(self):
        self.client.force_authenticate(user=self.user1)

        url = reverse("review_create")

        first_response = self.client.post(
            url,
            {
                "book": self.book.id,
                "rating": 5,
                "comment": "First review",
            },
            format="json",
        )

        print(first_response.data)

        self.assertEqual(
            first_response.status_code,
            status.HTTP_201_CREATED,
        )

        second_response = self.client.post(
            url,
            {
                "book": self.book.id,
                "rating": 2,
                "comment": "Duplicate review",
            },
            format="json",
        )

        self.assertEqual(
            second_response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            Review.objects.filter(
                book=self.book,
                user=self.user1,
            ).count(),
            1,
        )

    def test_current_user_returns_authenticated_user(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(reverse("current_user"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user1.id)
        self.assertEqual(response.data["username"], self.user1.username)


    def test_current_user_requires_authentication(self):
        response = self.client.get(reverse("current_user"))

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )