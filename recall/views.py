from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recall.models import Comment
from recall.serializers import CommentSerializer
from users_app.models import Student, Tutor
from courses_app.permissions import IsStudent, IsAuthorStudentOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsStudent, IsAuthorStudentOrReadOnly]

    def perform_create(self, serializer):
        student_id = self.request.data.get('student_id')
        created_at = self.request.data.get('created_at')
        updated_at = self.request.data.get('updated_at')
        tutor_id = self.request.data.get('tutor')
        text = self.request.data.get('text')

        tutor = None
        if tutor_id:
            try:
                tutor = Tutor.objects.get(id=tutor_id)
            except ObjectDoesNotExist:
                raise ValueError(f"Tutor with id '{tutor_id}' does not exist.")

        serializer.save(student=self.request.user.student, tutor=tutor, text=text, created_at=created_at, updated_at=updated_at)
