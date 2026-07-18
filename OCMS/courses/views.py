from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .models import Course
from .serializers import CourseSerializer


@extend_schema(responses=CourseSerializer(many=True))
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def course_list(request):

    if request.method == 'GET':
        courses = Course.objects.all()

        ordering = request.query_params.get('ordering')
        title = request.query_params.get('title')

        if ordering:
            courses = courses.order_by(ordering)

        if title:
            courses = courses.filter(title__icontains=title)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_courses = paginator.paginate_queryset(courses, request)

        serializer = CourseSerializer(paginated_courses, many=True)
        return paginator.get_paginated_response(serializer.data)

    if request.method == 'POST':
        # Only Instructors and Admins can create courses
        if not hasattr(request.user, 'profile') or request.user.profile.role not in ['Instructor', 'Admin']:
            return Response({'error': 'Permission denied.'}, status=403)

        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            # Automatically assign the instructor if it's an Instructor creating it
            if request.user.profile.role == 'Instructor':
                serializer.save(instructor=request.user)
            else:
                serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


@extend_schema(responses=CourseSerializer)
@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def course_detail(request, id):
    try:
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        return Response({'error':'Not found'}, status=404)

    if request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    # Check permission for PUT, PATCH, DELETE
    if request.method in ['PUT', 'PATCH', 'DELETE']:
        if not hasattr(request.user, 'profile'):
            return Response({'error': 'Permission denied.'}, status=403)
        
        role = request.user.profile.role
        if role == 'Student':
            return Response({'error': 'Permission denied.'}, status=403)
        if role == 'Instructor' and course.instructor != request.user:
            return Response({'error': 'You can only modify your own courses.'}, status=403)

    if request.method == 'PUT':
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == 'PATCH':
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        course.delete()
        return Response({'message':'deleted'}, status=204)