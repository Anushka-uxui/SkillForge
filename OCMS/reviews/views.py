from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .models import Review
from .serializers import ReviewSerializer


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def review_list(request):

    if request.method == 'GET':
        reviews = Review.objects.all()

        rating = request.query_params.get('rating')

        if rating:
            reviews = reviews.filter(rating=rating)

        paginator = PageNumberPagination()
        paginator.page_size = 2
        paginated = paginator.paginate_queryset(reviews, request)

        serializer = ReviewSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)

    if request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def review_detail(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response({'error':'Not found'}, status=404)

    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    if request.method == 'PATCH':
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    if request.method == 'DELETE':
        review.delete()
        return Response({'message':'deleted'}, status=204)