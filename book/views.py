from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from .models import Book, Author, Category, Review
from .forms import BookForm
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from .serializers import BookSerializer, AuthorSerializer, CategorySerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

# Create your views here.

class book_paginator(PageNumberPagination) :
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET'])
def book_list(request) :
    books = Book.objects.all()
    paginator = book_paginator()
    page = paginator.paginate_queryset(books, request)
    serilizer = BookSerializer(page, many=True)
    return paginator.get_paginated_response(serilizer.data)


@api_view(['GET'])
def books_info(request, id) :
    the_book = get_object_or_404(Book , id=id)
    serilizer = BookSerializer(the_book)
    return Response(serilizer.data)



@extend_schema(
    request=BookSerializer,
    responses=BookSerializer
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_book(request) :
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid() :
        serializer.save()
        return JsonResponse({'added' : 'successfull'} , status = 201)
    else :
        return JsonResponse(serializer.errors , status=400)




@extend_schema(
    request=BookSerializer,
    responses=BookSerializer
)
@api_view(["PUT" , "PATCH"])
@permission_classes([IsAuthenticated])
def update_book(request, id) :
    if request.method == 'PUT' :
        the_book = get_object_or_404(Book,id=id)
        
        serialiser = BookSerializer(the_book , data = request.data)
        if serialiser.is_valid() :
            serialiser.save()
            return JsonResponse({'updated' : 'successfull'} , status =200)
        return JsonResponse(serialiser.errors , status=400)
    
    if request.method == 'PATCH' :
        the_book = get_object_or_404(Book,id=id)
       
        serialiser = BookSerializer(the_book , data = request.data , partial = True)
        if serialiser.is_valid() :
            serialiser.save()
            return JsonResponse({'updated' : 'successfull'} , status =200)
        return JsonResponse(serialiser.errors , status=400)
    


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_book(request , id) :
    the_book = get_object_or_404(Book , id=id)
    the_book.delete()
    return Response(status = 204)




@extend_schema(
    parameters=[
        OpenApiParameter(
            name='title',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description='Filter by book title',
        ),
        OpenApiParameter(
            name='author',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description='Filter by author name',
        ),
        OpenApiParameter(
            name='category',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description='Filter by category name',
        ),
    ]
)
@api_view(['GET'])
def filter_book(request) :

    result = Book.objects.all()

    title = request.query_params.get('title')
    author = request.query_params.get('author')
    category = request.query_params.get('category')


    if title :
        result = result.filter(title__icontains = title)

    if author:
        if author.isdigit():
            result = result.filter(author__id=int(author))
        else:
            result = result.filter(author__name__icontains=author)

        result = result.distinct()

    if category :
        result = result.filter(category__name__icontains=category)

    paginator = book_paginator()
    page = paginator.paginate_queryset(result, request)

    serializer = BookSerializer(page, many=True)

    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def author_list(request):
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def author_info(request, id) :
    the_author = get_object_or_404(Author, id = id)
    serializer = AuthorSerializer(the_author)
    return Response(serializer.data)


@extend_schema(
    request=AuthorSerializer,
    responses=AuthorSerializer
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_author(request) :
    serializer = AuthorSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({'created' : 'successfull'} , status = 201)
    
    else :
        return Response(serializer.errors , status=400)
    


@extend_schema(
    request=AuthorSerializer,
    responses=AuthorSerializer
)
@api_view(['PUT' , 'PATCH'])
@permission_classes([IsAuthenticated])
def update_author(request, id) :
    if request.method == 'PUT' :
        the_author = get_object_or_404(Author,id=id)
        
        serialiser = AuthorSerializer(the_author , data = request.data)
        if serialiser.is_valid() :
            serialiser.save()
            return JsonResponse({'updated' : 'successfull'} , status =200)
        return JsonResponse(serialiser.errors , status=400)
    
    if request.method == 'PATCH' :
        the_author = get_object_or_404(Author,id=id)
        
        serialiser = AuthorSerializer(the_author , data = request.data, partial = True)
        if serialiser.is_valid() :
            serialiser.save()
            return JsonResponse({'updated' : 'successfull'} , status =200)
        return JsonResponse(serialiser.errors , status=400)
    


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_author(request , id) :
    the_author = get_object_or_404(Author , id=id)
    the_author.delete()
    return Response(status = 204)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_info(request, id) :
    the_category = get_object_or_404(Category,id = id)
    serializer = CategorySerializer(the_category)
    return Response(serializer.data)


@extend_schema(
    request=CategorySerializer,
    responses=CategorySerializer
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_category(request) :
    serializer = CategorySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({'created' : 'successfull'} , status = 201)
    else :
        return Response(serializer.errors , status = 400)
    


@extend_schema(
    request=CategorySerializer,
    responses=CategorySerializer
)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_category(request, id) :
    if request.method == 'PUT' :
        the_category = get_object_or_404(Category,id=id)
        
        serialiser = CategorySerializer(the_category , data = request.data)
        if serialiser.is_valid() :
            serialiser.save()
            return JsonResponse({'updated' : 'successfull'} , status =200)
        return JsonResponse(serialiser.errors , status=400)
    
    if request.method == 'PATCH' :
        the_category = get_object_or_404(Category,id=id)
        
        serialiser = CategorySerializer(the_category , data = request.data, partial = True)
        if serialiser.is_valid() :
            serialiser.save()
            return JsonResponse({'updated' : 'successfull'} , status =200)
        return JsonResponse(serialiser.errors , status=400)
    


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_category(request , id) :
    the_category = get_object_or_404(Category , id=id)
    the_category.delete()
    return Response(status = 204)



@extend_schema(
    tags=['reviews'],
    parameters=[
        OpenApiParameter(
            name='id',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            required=True,
            description='ID of the book',
        )
    ],
    responses=ReviewSerializer(many=True),
)
@api_view(['GET'])
def the_review_list(request, id):
    book = get_object_or_404(Book , id=id)
    reviews = Review.objects.filter(book=book)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)



@extend_schema(
    request=ReviewSerializer,
    responses=ReviewSerializer
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request):
    serializer = ReviewSerializer(
        data=request.data,
        context={'request': request},
    )

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)



@extend_schema(
    request=ReviewSerializer,
    responses=ReviewSerializer
)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_review(request, id):
    review = get_object_or_404(Review, id=id)

    if review.user != request.user:
        return Response(
            {'detail': 'You cannot edit another user\'s review.'},
            status=403
        )

    partial = request.method == 'PATCH'
    serializer = ReviewSerializer(
        review,
        data=request.data,
        context={'request': request},
        partial=partial
    )

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)

    return Response(serializer.errors, status=400)   


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_review(request, id):
    review = get_object_or_404(Review, id=id)

    if review.user != request.user:
        return Response(
            {'detail': 'You cannot delete another user\'s review.'},
            status=403
        )

    review.delete()
    return Response(status=204)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user

    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
    })