from tabnanny import check
from django.contrib.auth.models import AbstractUser
from django.db import models

class UserE(AbstractUser):
    sent_reports = models.BooleanField(null = True)
    is_admin = models.BooleanField(null = True)


class Exercise(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    link_video = models.TextField()
    id_link_video = models.TextField(null = True)
    category = models.CharField(max_length=255)
    duration = models.IntegerField()
    equipment = models.BooleanField()
    dificulty = models.IntegerField()
    approved = models.BooleanField(default=False)
    user_id = models.ForeignKey(UserE, on_delete=models.CASCADE, related_name="excercise_request_owner", null = True, default=None)
    admin_id = models.ForeignKey(UserE, on_delete=models.CASCADE, related_name="assessor", null = True, default=None)
    
    
class Routine(models.Model):
    name = models.CharField(max_length=200)
    duration = models.IntegerField(null = True, default=None)
    user_id = models.ForeignKey(UserE, on_delete=models.CASCADE, related_name="routine_owner")


class RoutineDay(models.Model):
    day_of_week = models.IntegerField()
    start_hour = models.TextField()
    routine_id = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name="routine_per_day")
        

class RoutineExcercise(models.Model):
    position = models.IntegerField(null = True, default=None)
    repetitions = models.IntegerField(null = True, default=1)
    routine_id = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name="routine_excercise_owner")
    excercise_id = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="includes")
    
# Create your models here.
