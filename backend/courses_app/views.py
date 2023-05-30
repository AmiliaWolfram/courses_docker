from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta

from users_app.models import Tutor, Student
from courses_app.models import Course, Language
from courses_app.serializers import CourseSerializer, LanguageSerializer
from courses_app.permissions import IsTutor, IsAuthorTutorOrReadOnly


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    # permission_classes = [IsTutor, ]
    permission_classes = [IsTutor, IsAuthenticated, IsAuthorTutorOrReadOnly]

    def perform_create(self, request):
        language_id = request.data.get('language')
        level = request.data.get('level')
        students_id = request.data.get('students')
        date_started = request.data.get('date_started')
        duration = request.data.get('duration')
        date_ended = request.data.get('date_ended')
        tutor_id = request.data.get('tutor_id')

        tutor = None
        if tutor_id:
            tutor = get_object_or_404(Tutor, id=tutor_id)

        try:
            language = Language.objects.get(id=language_id)
        except Language.DoesNotExist:
            return Response({"error": "Invalid language ID"}, status=status.HTTP_400_BAD_REQUEST)

        students = get_object_or_404(Student, id=students_id)

        course = Course(
            language=language,
            level=level,
            students=students,
            date_started=date_started,
            duration=duration,
            date_ended=date_ended,
            tutor=self.request.user.tutor
        )
        course.save()

        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def perform_update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #
    #     # Convert date_started to string
    #     date_started = instance.date_started.strftime('%Y-%m-%dT%H:%M:%S')
    #
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     return Response(serializer.data)


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsTutor, IsAuthenticated, ]
