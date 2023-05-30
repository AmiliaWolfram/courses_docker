from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from courses_app.permissions import IsStudent
from .models import User, Tutor, Student, Vote, VoteType
from .serializers import StudentRegisterSerializer, TutorRegisterSerializer, \
    TutorSerializer, StudentSerializer, VoteSerializer, VoteTypeSerializer


class UserStudentRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = StudentRegisterSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]


class UserTutorRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = TutorRegisterSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]


class TutorListAPIView(generics.ListAPIView):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]


class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]


class RegistrationTutorRequestAPIView(generics.CreateAPIView):
    queryset = Tutor.objects.all()
    serializer_class = TutorRegisterSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]


class VoteTypeCreateAPIView(generics.CreateAPIView):
    queryset = VoteType.objects.all()
    serializer_class = VoteTypeSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser, ]


class VoteCreateAPIView(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsStudent, ]

    def perform_create(self, serializer):
        serializer.save(
            student=self.request.user.student,
            tutor=get_object_or_404(Tutor, pk=self.kwargs['tutor'])
        )
