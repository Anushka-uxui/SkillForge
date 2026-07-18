from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.core.mail import send_mail
from django.conf import settings
from .models import Enrollment
from .serializers import EnrollmentSerializer
from courses.models import Course

@extend_schema(responses=EnrollmentSerializer(many=True))
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def enrollment_list(request):
    if request.method == 'GET':
        enrollments = Enrollment.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 2
        paginated = paginator.paginate_queryset(enrollments, request)
        serializer = EnrollmentSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)

    if request.method == 'POST':
        # Only Admins can manually create enrollments via this endpoint
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'Admin':
            return Response({'error': 'Permission denied.'}, status=403)
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@extend_schema(responses=EnrollmentSerializer)
@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def enrollment_detail(request, id):
    try:
        enrollment = Enrollment.objects.get(id=id)
    except Enrollment.DoesNotExist:
        return Response({'error':'Not found'}, status=404)

    # Only Admins can view/edit specific enrollment details via this endpoint
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'Admin':
        return Response({'error': 'Permission denied.'}, status=403)

    if request.method == 'GET':
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = EnrollmentSerializer(enrollment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == 'PATCH':
        serializer = EnrollmentSerializer(enrollment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        enrollment.delete()
        return Response({'message':'deleted'}, status=204)

@extend_schema(responses={200: {'description': 'Enrolled successfully'}})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enroll_course(request, course_id):
    # Only Students and Admins can enroll
    if not hasattr(request.user, 'profile') or request.user.profile.role not in ['Student', 'Admin']:
        return Response({'error': 'Only students can enroll in courses.'}, status=403)

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"message": "Course not found"}, status=404)

    # prevent duplicate enroll (fixed field name from 'user' to 'student')
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        return Response({"message": "Already enrolled"}, status=400)

    Enrollment.objects.create(student=request.user, course=course)

    # Send email notification
    subject = f"Enrolled in {course.title}"
    message = f"Hello {request.user.username},\n\nYou have successfully enrolled in the course '{course.title}'.\n\nHappy Learning!"
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [request.user.email],
            fail_silently=True,
        )
    except Exception as e:
        # Ignore email sending errors so we don't break the response
        pass

    return Response({"message": "Enrolled successfully"})