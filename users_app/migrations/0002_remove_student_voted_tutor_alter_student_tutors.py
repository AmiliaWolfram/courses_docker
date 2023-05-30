# Generated by Django 4.2 on 2023-05-30 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='voted_tutor',
        ),
        migrations.AlterField(
            model_name='student',
            name='tutors',
            field=models.ManyToManyField(related_name='students', to='users_app.tutor'),
        ),
    ]