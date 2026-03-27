from django.urls import path
from .views import StudentListCreateAPI, StudentDetailAPI

urlpatterns = [
    path('students/', StudentListCreateAPI.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentDetailAPI.as_view(), name='student-detail'),
]