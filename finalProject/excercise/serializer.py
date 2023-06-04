from rest_framework import serializers
from excercise.models import RoutineExcercise
from excercise.models import Exercise

class AuxExecisePosition:
  def __init__(self, exercise, routineExcercise):
    self.Exercise = exercise
    self.RoutineExcercise = routineExcercise

class RoutineExcerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineExcercise
        fields = '__all__'

class AuxExecisePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuxExecisePosition
        fields = '__all__'