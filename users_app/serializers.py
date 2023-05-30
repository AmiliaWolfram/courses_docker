from django.db import IntegrityError, transaction
from rest_framework import serializers

from users_app.models import User, Tutor, Student, Vote, VoteType
from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class StudentRegisterSerializer(serializers.ModelSerializer):
    tutors = serializers.PrimaryKeyRelatedField(many=True, queryset=Tutor.objects.all())
    password = serializers.CharField(max_length=20, write_only=True)
    password2 = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "password2",
                  "first_name", "last_name", "profile_image", "age", "tutors"]

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords don't match")
        if len(data['password']) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")
        if data['password'].isdigit():
            raise serializers.ValidationError("Password must contain letters")
        if not any(char.isupper() for char in data['password']) or not any(char.islower() for char in data['password']):
            raise serializers.ValidationError("Password must contain both uppercase and lowercase letters")
        return data

    # def create(self, validated_data):
    #     user = User(
    #         username=validated_data['username'],
    #         first_name=validated_data['first_name'],
    #         last_name=validated_data['last_name'],
    #         age=validated_data['age']
    #     )
    #     profile_image = validated_data.get('profile_image')
    #     if profile_image:
    #         user.profile_image = profile_image
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     try:
    #         student = Student.objects.create(user=user)
    #     except Exception as e:
    #         user.delete()
    #         raise e
    #     else:
    #         student.username = user.username
    #         student.profile_image = user.profile_image
    #         student.age = user.age
    #     return student

    @transaction.atomic
    def create(self, validated_data):
        tutors_data = validated_data.pop('tutors', [])
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        student = Student.objects.create(user=user)
        student.tutors.set(tutors_data)
        student.username = user.username
        student.profile_image = user.profile_image
        student.age = user.age
        student.save()
        return student


class TutorRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, write_only=True)
    password2 = serializers.CharField(max_length=20, write_only=True)
    experience = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ["username", "password", "password2",
                  "first_name", "last_name", "profile_image", "age", "experience"]

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords don't match")
        if len(data['password']) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")
        if data['password'].isdigit():
            raise serializers.ValidationError("Password must contain letters")
        if not any(char.isupper() for char in data['password']) or not any(char.islower() for char in data['password']):
            raise serializers.ValidationError("Password must contain both uppercase and lowercase letters")
        if data['age'] < 18:
            raise serializers.ValidationError("The tutor can't be under 18 years of age.")
        if int(data['age']) < int(data['experience']):
            raise serializers.ValidationError("Experience can't be greater than your age!")
        residual = int(data['age']) - int(data['experience'])
        if residual < 18:
            raise serializers.ValidationError("You couldn't start working before the age og 18!")
        return data

    @transaction.atomic
    def create(self, validated_data):
        students_data = validated_data.pop('students', [])
        print(f"students_data: {students_data}")
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        experience = validated_data.pop('experience')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        tutor = Tutor.objects.create(user=user, experience=experience)
        tutor.students.set(students_data)
        tutor.username = user.username
        tutor.profile_image = user.profile_image
        tutor.age = user.age
        tutor.save()
        return tutor

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)

    # def create(self, validated_data):
    #     user = User(
    #         username=validated_data['username'],
    #         first_name=validated_data['first_name'],
    #         last_name=validated_data['last_name'],
    #         age=validated_data['age']
    #     )
    #     profile_image = validated_data.get('profile_image')
    #     if profile_image:
    #         user.profile_image = profile_image
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     try:
    #         tutor = Tutor.objects.create(user=user, experience=validated_data['experience'])
    #     except Exception as e:
    #         user.delete()
    #         raise e
    #     else:
    #         tutor.username = user.username
    #         tutor.profile_image = user.profile_image
    #         tutor.age = user.age
    #     return tutor
    #
    # @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    # def create_auth_token(sender, instance=None, created=False, **kwargs):
    #     if created:
    #         Token.objects.create(user=instance)


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class VoteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteType
        fields = '__all__'
        read_only_fields = ['student', 'tutor', ]


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
        read_only_fields = ['student', 'tutor']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            new_vote_type = validated_data.pop('vote')
            instance = self.Meta.model.objects.get(**validated_data)
            instance.vote = new_vote_type
            instance.save()
            return instance
