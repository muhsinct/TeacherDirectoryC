from django.db import models

# Create your models here.


class SubjectsMaster(models.Model):
    subject_name = models.CharField(max_length=100, null=False, unique=True)


class Profiles(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, null=False, unique=True)
    phone_number = models.CharField(max_length=20)
    room_number = models.CharField(max_length=5)
    image_name = models.ImageField(upload_to='profile_pictures', blank=True,
                                   default='profile_pictures/default/default_user.png')

    subjects = models.ManyToManyField(SubjectsMaster)

