
from datetime import date

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Author, Category, Book, Review


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = '__all__'

    def validate_published_year(self, value):
        if value is not None and not 1000 <= value <= date.today().year:
            raise serializers.ValidationError(
                'The year does not make sense!'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user', 'created_at']
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['book', 'user'],
                message='This user has already reviewed this book!'
            )
        ]

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError(
                'The rating must be between 1 and 5!'
            )
        return value
