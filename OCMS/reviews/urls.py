from django.urls import path
from .views import review_list, review_detail

urlpatterns = [
    path('', review_list),
    path('<int:id>/', review_detail),
]