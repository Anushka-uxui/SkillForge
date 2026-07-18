from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.db.models import Avg, Count
from courses.models import Course
from enrollments.models import Enrollment
from reviews.models import Review
from enrollments.serializers import EnrollmentSerializer
from courses.serializers import CourseSerializer

@extend_schema(responses={200: {'type': 'object'}})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def instructor_dashboard(request):
    """
    Returns dashboard metrics for the logged-in instructor.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'Instructor':
        return Response({'error': 'Permission denied. Only Instructors can view this dashboard.'}, status=403)
    
    instructor_courses = Course.objects.filter(instructor=request.user)
    
    total_courses = instructor_courses.count()
    
    total_enrollments = Enrollment.objects.filter(course__instructor=request.user).count()
    
    # Calculate average course rating
    avg_rating_dict = Review.objects.filter(course__instructor=request.user).aggregate(Avg('rating'))
    average_rating = avg_rating_dict['rating__avg'] or 0.0
    
    total_reviews = Review.objects.filter(course__instructor=request.user).count()
    
    recent_enrollments_qs = Enrollment.objects.filter(course__instructor=request.user).order_by('-enrolled_date')[:5]
    recent_enrollments = EnrollmentSerializer(recent_enrollments_qs, many=True).data
    
    most_popular_course_qs = instructor_courses.annotate(enrollment_count=Count('enrollment')).order_by('-enrollment_count').first()
    most_popular_course = CourseSerializer(most_popular_course_qs).data if most_popular_course_qs else None
    
    return Response({
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'average_rating': round(average_rating, 2),
        'total_reviews': total_reviews,
        'recent_enrollments': recent_enrollments,
        'most_popular_course': most_popular_course,
    })
