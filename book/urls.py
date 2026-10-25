
from django.urls import path
from book import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/users/me/" , views.current_user , name="current_user"),

    path("api/books/", views.book_list, name="book_list"),
    path("api/books/create/", views.add_book, name="book_create"),
    path("api/books/filter/", views.filter_book, name="book_filter"),
    path("api/books/<int:id>/", views.books_info, name="book_detail"),
    path("api/books/<int:id>/update/", views.update_book, name="book_update"),
    path("api/books/<int:id>/delete/", views.delete_book, name="book_delete"),

    path("api/authors/", views.author_list, name="author_list"),
    path("api/authors/create/", views.add_author, name="author_create"),
    path("api/authors/<int:id>/", views.author_info, name="author_detail"),
    path("api/authors/<int:id>/update/", views.update_author, name="author_update"),
    path("api/authors/<int:id>/delete/", views.delete_author, name="author_delete"),

    path("api/categories/", views.category_list, name="category_list"),
    path("api/categories/create/", views.add_category, name="category_create"),
    path("api/categories/<int:id>/", views.category_info, name="category_detail"),
    path("api/categories/<int:id>/update/", views.update_category, name="category_update"),
    path("api/categories/<int:id>/delete/", views.delete_category, name="category_delete"),

    path("api/books/<int:id>/reviews/", views.the_review_list, name="book_review_list"),
    path("api/reviews/create/", views.add_review, name="review_create"),
    path("api/reviews/<int:id>/update/", views.update_review, name="review_update"),
    path("api/reviews/<int:id>/delete/", views.delete_review, name="review_delete"),
]
