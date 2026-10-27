from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model) :
    name = models.CharField(max_length=100)
    bio = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model) :
    name = models.CharField(max_length=100 , unique=True)

    def __str__(self):
        return self.name


class Book(models.Model) :
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    published_year = models.IntegerField(null=True, blank=True)
    author = models.ManyToManyField(Author)
    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book , on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['book' , 'user'],
                name = 'book_user_unique_review'
            )
        ]
