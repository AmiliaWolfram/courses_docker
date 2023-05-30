# from rest_framework import serializers
# from rest_framework.generics import get_object_or_404
#
# from courses_app.models import Course, Language
# from users_app.models import Tutor
#
#
# class CourseSerializer(serializers.ModelSerializer):
#     tutor = serializers.ReadOnlyField(source='tutor.username.id')
#     class Meta:
#         model = Course
#         exclude = ['date_ended']
#
#
# class LanguageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Language
#         fields = '__all__'
# #******
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from courses_app.models import Course, Language
from users_app.models import Tutor


class CourseSerializer(serializers.ModelSerializer):
    tutor = serializers.ReadOnlyField(source='tutor.username.id')

    class Meta:
        model = Course
        exclude = ['date_ended']


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'
