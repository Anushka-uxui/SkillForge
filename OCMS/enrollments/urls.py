from django.urls import path
from .views import enrollment_list,enrollment_detail,enroll_course

urlpatterns = [
    path('', enrollment_list),
    path('<int:id>/', enrollment_detail),
    path('enroll/<int:course_id>/',enroll_course)
]