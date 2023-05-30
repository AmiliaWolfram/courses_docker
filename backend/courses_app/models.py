from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from datetime import timedelta, datetime
from dateutil.parser import parse

from users_app.models import Tutor, Student
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware

class Language(models.Model):
    denomination = models.CharField(max_length=20)

    def __str__(self):
        return self.denomination


@receiver(post_save, sender=Language)
@receiver(post_delete, sender=Language)
def update_language_field(sender, instance, **kwargs):
    courses = Course.objects.filter(language=instance)
    if not courses.exists():
        return
    if kwargs.get('created', True):
        # Language was added
        courses.update(language=instance)
    else:
        # Language was deleted
        default_language = Language.objects.first()  # Choose a default language to assign to the courses
        courses.update(language=default_language)


class Course(models.Model):
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)
    # language = models.ForeignKey(Language, on_delete=models.CASCADE)
    level = models.CharField(max_length=2, choices=[
            ('A1', 'A1'),
            ('A2', 'A2'),
            ('B1', 'B1'),
            ('B2', 'B2'),
            ('C1', 'C1'),
            ('C2', 'C2')
        ]
    )
    tutor = models.ForeignKey(Tutor, on_delete=models.SET_NULL, null=True, blank=True)
    # students = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    students = models.ManyToManyField(Student, blank=True)
    date_started = models.DateTimeField()
    duration = models.IntegerField(verbose_name='Duration in months')
    date_ended = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.date_started and self.duration:
            if self.date_started and self.duration:
                duration_days = int(self.duration) * 30
                self.date_ended = self.date_started + timedelta(days=duration_days)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.language.denomination} {self.level} Course'
