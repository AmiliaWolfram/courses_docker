from django.db import models
from django.contrib.auth.models import AbstractUser


def profile_image_store(instance, filename):
    return f'profile/{instance.username}/{filename}'


class User(AbstractUser):
    age = models.IntegerField(default=18)
    profile_image = models.ImageField(upload_to=profile_image_store, default='profile/default.png')

    def __str__(self):
        return self.username


class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    students = models.ManyToManyField('Student', related_name='tutor_set', related_query_name='tutor', blank=True)
    experience = models.IntegerField()

    @staticmethod
    def update_students(sender, instance, action, pk_set, **kwargs):
        if action == 'post_add':
            for student_id in pk_set:
                student = Student.objects.get(pk=student_id)
                student.tutors.add(instance)
        elif action == 'post_remove':
            for student_id in pk_set:
                student = Student.objects.get(pk=student_id)
                student.tutors.remove(instance)

    def __str__(self):
        return self.user.username

    def increment_votes(self):
        self.votes += 1
        self.save()


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    tutors = models.ManyToManyField(Tutor, related_name='student_set', related_query_name='student', blank=True)

    @staticmethod
    def update_tutors(sender, instance, action, pk_set, **kwargs):
        if action == 'post_add':
            for tutor_id in pk_set:
                tutor = Tutor.objects.get(pk=tutor_id)
                tutor.students.add(instance)
        elif action == 'post_remove':
            for tutor_id in pk_set:
                tutor = Tutor.objects.get(pk=tutor_id)
                tutor.students.remove(instance)

    def __str__(self):
        return self.user.username


class VoteType(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Vote(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='tutor_votes')
    vote = models.ForeignKey('VoteType', on_delete=models.SET_DEFAULT, default=1)

    def __str__(self):
        return f'{self.tutor} - {self.student} - {self.vote}'

    class Meta:
        unique_together = ['student', 'tutor']