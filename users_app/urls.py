from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('register/student/', views.UserStudentRegisterAPIView.as_view()),
    path('register/tutor/', views.RegistrationTutorRequestAPIView.as_view()),
    path('tutors/', views.TutorListAPIView.as_view()),
    path('students/', views.StudentListAPIView.as_view()),
    path('tutors/<int:tutor>/vote', views.VoteCreateAPIView.as_view()),
    path('token/', obtain_auth_token),
    path('auth', include('rest_framework.urls')),
]
