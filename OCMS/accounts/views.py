from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .models import Profile


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def profile_list(request):

    if request.method == 'GET':
        profiles = Profile.objects.all()

        name = request.query_params.get('name')

        if name:
            profiles = profiles.filter(name__icontains=name)

        paginator = PageNumberPagination()
        paginator.page_size = 2
        paginated_profiles = paginator.paginate_queryset(profiles, request)

        serializer = ProfileSerializer(paginated_profiles, many=True)
        return paginator.get_paginated_response(serializer.data)

    if request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def profile_detail(request, id):
    try:
        profile = Profile.objects.get(id=id)
    except Profile.DoesNotExist:
        return Response({'error':'Not found'}, status=404)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    if request.method == 'PATCH':
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    if request.method == 'DELETE':
        profile.delete()
        return Response({'message':'deleted'}, status=204)
    
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegisterSerializer

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"}, status=201)

    return Response(serializer.errors, status=400)