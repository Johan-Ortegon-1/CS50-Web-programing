from enum import Flag
import json
from random import choices
import sys
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from json import dumps
from django import forms
import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from excercise.serializer import RoutineExcerciseSerializer, AuxExecisePositionSerializer

from excercise.models import *
from django.core.validators import MaxValueValidator, MinValueValidator

from typing import List

import traceback



CATEGORY_OPTIONS = [
    ('chest','Chest'),
    ('back','Back'),
    ('arms','Arms'),
    ('shoulders','Shoulders'),
    ('legs','Legs'),
    ('calves','Calves'),
    ('cardio','Cardio'),
    ('flexibility','Flexibility'),
    ('other', 'Other')
]

FILTER_CATEGORY_OPTIONS = [
    ('all', 'All'),
    ('chest','Chest'),
    ('back','Back'),
    ('arms','Arms'),
    ('shoulders','Shoulders'),
    ('legs','Legs'),
    ('calves','Calves'),
    ('cardio','Cardio'),
    ('flexibility','Flexibility'),
    ('other', 'Other')
]

DIFICULTY_OPTIONS = [
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5')
]

FILTER_DIFICULTY_OPTIONS = [
    ('all', 'All'),
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5')
]

class RequestExerciseForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    desciption = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=True)
    video_url = forms.URLField(widget=forms.URLInput(attrs={'class':'form-control'}), required=True)
    listing_category = forms.CharField(widget=forms.Select(attrs={'class':'form-control'}, choices = CATEGORY_OPTIONS), required=True)
    duration = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control', 'min':1,'max': 100,'type': 'number'}))
    equipment = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-control'}), required=False)
    listing_dificulty = forms.CharField(widget=forms.Select(attrs={'class':'form-control'}, choices = DIFICULTY_OPTIONS), required=True)


class SearchByNameForm(forms.Form):
    search_input = forms.CharField(widget=forms.TextInput())


class ExploreFilterForm(forms.Form):
    min_duration = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'row form-control', 'min':1,'max': 100,'type': 'number', 'onchange':"document.getElementById('filter-explore-form').submit()"}), required=False)
    max_duration = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'row form-control', 'min':1,'max': 100,'type': 'number', 'onchange':"document.getElementById('filter-explore-form').submit()"}), required=False)
    category = forms.CharField(widget=forms.Select(attrs={'class':'row  form-control', 'onchange':"document.getElementById('filter-explore-form').submit()"}, choices = FILTER_CATEGORY_OPTIONS), required=False)
    dificulty = forms.CharField(widget=forms.Select(attrs={'class':'row  form-control', 'onchange':"document.getElementById('filter-explore-form').submit()"}, choices = FILTER_DIFICULTY_OPTIONS), required=False)
    equipment = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'row  form-control', 'onchange':"document.getElementById('filter-explore-form').submit()"}), required=False)


class CreateRoutineForm(forms.Form):
    routine_title = forms.CharField(widget=forms.TextInput(), required=True)
    sun_chb = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    sun_s_t = forms.CharField(widget=forms.TextInput(), required=False)
    mon_chb = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    mon_s_t = forms.CharField(widget=forms.TextInput(), required=False)
    tue_chb = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    tue_s_t = forms.CharField(widget=forms.TextInput(), required=False)
    wed_chb = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    wed_s_t = forms.CharField(widget=forms.TextInput(), required=False)
    thu_chb = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    thu_s_t = forms.CharField(widget=forms.TextInput(), required=False)
    fri_chb = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    fri_s_t = forms.CharField(widget=forms.TextInput(), required=False)
    sat_chb = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    sat_s_t = forms.CharField(widget=forms.TextInput(), required=False)
    routine_id = forms.IntegerField(widget=forms.NumberInput(), required=False)


class AddExerciseRoutine(forms.Form):
    slc_routine = forms.CharField(widget=forms.Select(), required=False)
    id_exercise = forms.IntegerField(widget=forms.NumberInput(), required=False)

class AuxRoutine():
    def __init__(self, name, start_hour, end_hour, id):
        self.Name = name
        self.Start_hour = start_hour
        self.End_hour = end_hour
        self.Id = id
        
class AuxExecisePosition:
  def __init__(self, exercise, routineExcercise):
    self.Exercise = exercise
    self.RoutineExcercise = routineExcercise

class AuxSerializableExecisePosition:
  def __init__(self, auxiliars: List[AuxExecisePosition]):
    self.auxiliars = auxiliars

class AuxRoutineRDay:
    def __init__(self, routine, routineDay):
        self.routine = routine
        self.routineDay = routineDay

def index(request):
    
    mon_array = []
    tue_array = []
    wed_array = []
    thu_array = []
    fri_array = []
    sat_array = []
    sun_array = []
    
    if request.method == "POST" and 'btn_create' in request.POST:
        print(sys.stderr, "Creating a routine flag")
        form = CreateRoutineForm(request.POST)
        if form.is_valid():
            
            routine_title = form.cleaned_data["routine_title"]
            
            sun_chb = form.cleaned_data["sun_chb"]
            sun_s_t = form.cleaned_data["sun_s_t"]
            mon_chb = form.cleaned_data["mon_chb"]
            mon_s_t = form.cleaned_data["mon_s_t"]
            tue_chb = form.cleaned_data["tue_chb"]
            tue_s_t = form.cleaned_data["tue_s_t"]
            wed_chb = form.cleaned_data["wed_chb"]
            wed_s_t = form.cleaned_data["wed_s_t"]
            thu_chb = form.cleaned_data["thu_chb"]
            thu_s_t = form.cleaned_data["thu_s_t"]
            fri_chb = form.cleaned_data["fri_chb"]
            fri_s_t = form.cleaned_data["fri_s_t"]
            sat_chb = form.cleaned_data["sat_chb"]
            sat_s_t = form.cleaned_data["sat_s_t"]
                        
            p_user_id = request.user
            
            new_routine = Routine(name = routine_title, duration = 30, user_id = p_user_id)
            
            # Attempt to create new routine
            try:
                new_routine.save()
            except IntegrityError as e:
                message = traceback.format_exc()
                print(sys.stderr, message)

                return render(request, "excercise/create_routine.html", {
                    "message": "Error creating the request for a new Routine",
                    "requestExerciseForm":form
                })
            
            # Attempt to create the RoutineDay
            try:
                if mon_chb:
                    new_day_routine = RoutineDay(day_of_week = 1, start_hour = mon_s_t, routine_id = new_routine)
                    new_day_routine.save()
                if tue_chb:
                    new_day_routine = RoutineDay(day_of_week = 2, start_hour = tue_s_t, routine_id = new_routine)
                    new_day_routine.save()
                if wed_chb:
                    new_day_routine = RoutineDay(day_of_week = 3, start_hour = wed_s_t, routine_id = new_routine)
                    new_day_routine.save()
                if thu_chb:
                    new_day_routine = RoutineDay(day_of_week = 4, start_hour = thu_s_t, routine_id = new_routine)
                    new_day_routine.save()
                if fri_chb:
                    new_day_routine = RoutineDay(day_of_week = 5, start_hour = fri_s_t, routine_id = new_routine)
                    new_day_routine.save()
                if sat_chb:
                    new_day_routine = RoutineDay(day_of_week = 6, start_hour = sat_s_t, routine_id = new_routine)
                    new_day_routine.save()
                if sun_chb:
                    new_day_routine = RoutineDay(day_of_week = 7, start_hour = sun_s_t, routine_id = new_routine)
                    new_day_routine.save()
            except IntegrityError as e:
                message = traceback.format_exc()
                print(sys.stderr, message)
                return render(request, "excercise/create_routine.html", {
                    "message": "Error creating the request for Days Routine",
                    "requestExerciseForm":form
                })
    
    if request.method == "POST" and 'btn_edit' in request.POST:
        form = CreateRoutineForm(request.POST)
        if form.is_valid():
            
            routine_title = form.cleaned_data["routine_title"]
            
            sun_chb = form.cleaned_data["sun_chb"]
            sun_s_t = form.cleaned_data["sun_s_t"]
            mon_chb = form.cleaned_data["mon_chb"]
            mon_s_t = form.cleaned_data["mon_s_t"]
            tue_chb = form.cleaned_data["tue_chb"]
            tue_s_t = form.cleaned_data["tue_s_t"]
            wed_chb = form.cleaned_data["wed_chb"]
            wed_s_t = form.cleaned_data["wed_s_t"]
            thu_chb = form.cleaned_data["thu_chb"]
            thu_s_t = form.cleaned_data["thu_s_t"]
            fri_chb = form.cleaned_data["fri_chb"]
            fri_s_t = form.cleaned_data["fri_s_t"]
            sat_chb = form.cleaned_data["sat_chb"]
            sat_s_t = form.cleaned_data["sat_s_t"]
            
            p_routine = form.cleaned_data['routine_id']
            
            current_routine = Routine.objects.get(id = int(p_routine))
            
            
            # Attempt to update the RoutineDays
            try:
                if mon_chb:
                    RoutineDay.objects.update_or_create(day_of_week = 1, routine_id = current_routine, defaults={'start_hour':mon_s_t})
                else:
                    RoutineDay.objects.filter(day_of_week = 1, routine_id = current_routine).delete()
                if tue_chb:
                    RoutineDay.objects.update_or_create(day_of_week = 2, routine_id = current_routine, defaults={'start_hour':tue_s_t})
                else:
                    RoutineDay.objects.filter(day_of_week = 2, routine_id = current_routine).delete()
                if wed_chb:
                    RoutineDay.objects.update_or_create(day_of_week = 3, routine_id = current_routine, defaults={'start_hour':wed_s_t})
                else:
                    RoutineDay.objects.filter(day_of_week = 3, routine_id = current_routine).delete()
                if thu_chb:
                    RoutineDay.objects.update_or_create(day_of_week = 4, routine_id = current_routine, defaults={'start_hour':thu_s_t})
                else:
                    RoutineDay.objects.filter(day_of_week = 4, routine_id = current_routine).delete()
                if fri_chb:
                    RoutineDay.objects.update_or_create(day_of_week = 5, routine_id = current_routine, defaults={'start_hour':fri_s_t})
                else:
                    RoutineDay.objects.filter(day_of_week = 5, routine_id = current_routine).delete()
                if sat_chb:
                    RoutineDay.objects.update_or_create(day_of_week = 6, routine_id = current_routine, defaults={'start_hour':sat_s_t})
                else:
                    RoutineDay.objects.filter(day_of_week = 6, routine_id = current_routine).delete()
                if sun_chb:
                    RoutineDay.objects.update_or_create(day_of_week = 7, routine_id = current_routine, defaults={'start_hour':sun_s_t})
                else:
                    RoutineDay.objects.filter(day_of_week = 7, routine_id = current_routine).delete()
            except IntegrityError as e:
                message = traceback.format_exc()
                print(sys.stderr, message)
                return render(request, "excercise/index.html")
            
            # Attempt to update title routine
            try:
                Routine.objects.filter(id = p_routine).update(name = routine_title)
            except IntegrityError as e:
                print(sys.stderr, message)
                return render(request, "excercise/create_routine.html", {
                    "message": "Error creating the request for a new Routine",
                    "requestExerciseForm":form
                })
    
    if request.user.is_authenticated:
        current_user = request.user
        all_routines_by_user = Routine.objects.filter(user_id = current_user)
        for iter in all_routines_by_user:
            all_routine_days_by_routine = RoutineDay.objects.filter(routine_id = iter)
            for iter2 in all_routine_days_by_routine:
                new_aux_routine = AuxRoutine(iter.name, iter2.start_hour, calEndHour(iter2.start_hour, iter.duration), iter.id)
                if iter2.day_of_week == 1:
                    mon_array.append(new_aux_routine)
                elif iter2.day_of_week == 2:
                    tue_array.append(new_aux_routine)
                elif iter2.day_of_week == 3:
                    wed_array.append(new_aux_routine)
                elif iter2.day_of_week == 4:
                    thu_array.append(new_aux_routine)
                elif iter2.day_of_week == 5:
                    fri_array.append(new_aux_routine)
                elif iter2.day_of_week == 6:
                    sat_array.append(new_aux_routine)
                elif iter2.day_of_week == 7:
                    sun_array.append(new_aux_routine)
            
        
        return render(request, "excercise/index.html", {
                    "mon_array": mon_array,
                    "tue_array": tue_array,
                    "wed_array": wed_array,
                    "thu_array": thu_array,
                    "fri_array": fri_array,
                    "sat_array": sat_array,
                    "sun_array": sun_array
                })
    else:
        return render(request, "excercise/index.html", {
                    "user_flag": True,
                    "mon_array": [],
                    "tue_array": [],
                    "wed_array": [],
                    "thu_array": [],
                    "fri_array": [],
                    "sat_array": [],
                    "sun_array": []
                })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "excercise/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "excercise/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "excercise/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = UserE.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "excercise/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "excercise/register.html")


def explore(request):
    print(sys.stderr, "Method Flag")
    
    '''Seacrg Form code'''
    if request.method == "POST" and 'search_input' in request.POST:
        print(sys.stderr, "IF Search Flag")
        form = SearchByNameForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["search_input"]
            return render(request, "excercise/explore.html", {
                "items": Exercise.objects.filter(approved=True, name__icontains=title),
                "items_review": Exercise.objects.filter(approved=False),
                "exploreFilterForm":ExploreFilterForm()
            })
            
    '''Filter Form code'''
    if request.method == "POST" and 'filter-explore-form' in request.POST:
        form = ExploreFilterForm(request.POST)
        if form.is_valid():
            p_min_duration = form.cleaned_data["min_duration"]
            print(sys.stderr, "Empty duration: ", p_min_duration)
            p_max_duration = form.cleaned_data["max_duration"]
            p_category = form.cleaned_data["category"]
            print(sys.stderr, "Empty category: " + p_category)
            p_dificulty = form.cleaned_data["dificulty"]
            print(sys.stderr, "Empty dificulty: " + p_dificulty)
            p_equipment = form.cleaned_data["equipment"]
            print(sys.stderr, "Empty equipment: ", p_equipment)
            
            ''' Sequencial filters '''
            exercises = Exercise.objects.filter(approved=True)
            
            if p_min_duration != None:
                exercises = exercises.filter(duration__gte=p_min_duration)
            if p_max_duration != None:
                exercises = exercises.filter(duration__lte=p_max_duration)
            if p_category != "all":
                exercises = exercises.filter(category=p_category)
            if p_dificulty != "all":
                exercises = exercises.filter(dificulty=p_dificulty)
            if p_equipment == True:
                exercises = exercises.filter(equipment=p_equipment)
            
            return render(request, "excercise/explore.html", {
                "items": exercises,
                "items_review": Exercise.objects.filter(approved=False),
                "exploreFilterForm":form
            })

    return render(request, "excercise/explore.html", {
            "items": Exercise.objects.filter(approved=True),
            "items_review": Exercise.objects.filter(approved=False),
            "exploreFilterForm":ExploreFilterForm()
        })


def request(request):
    if request.method == "POST":
        formRequest = RequestExerciseForm(request.POST)
        if formRequest.is_valid():
            p_name = formRequest.cleaned_data["name"]
            p_desciption = formRequest.cleaned_data["desciption"]
            p_video_url = formRequest.cleaned_data["video_url"]
            p_listing_category = formRequest.cleaned_data["listing_category"]
            p_duration = formRequest.cleaned_data["duration"]
            p_equipment = formRequest.cleaned_data["equipment"]
            p_listing_dificulty = formRequest.cleaned_data["listing_dificulty"]            
            p_user_id = request.user
            
            p_admin = UserE.objects.get(username='admin1')
            
            exercise_request = Exercise(name = p_name, description = p_desciption, link_video = p_video_url, category = p_listing_category, duration = p_duration, equipment = p_equipment, dificulty = p_listing_dificulty, approved = False, user_id = p_user_id, admin_id = p_admin)
            
            # Attempt to create new listing
            try:
                exercise_request.save()
            except IntegrityError as e:
                message = traceback.format_exc()
                print(sys.stderr, message)

                return render(request, "excercise/request.html", {
                    "message": "Error creating the request",
                    "requestExerciseForm":RequestExerciseForm()
                })
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "excercise/request.html", {
                "message": "Invalid form"
            })
        
    return render(request, "excercise/request.html",  
                  {"requestExerciseForm":RequestExerciseForm()})


def review_request(request):
    return render(request, "excercise/explore.html", {
            "items": Exercise.objects.filter(approved=False)
        })


def exercise_detail(request, exercise_id):    
    '''SQL Queries'''
    currrent_excercise = Exercise.objects.get(id=exercise_id)
    
    '''Populating the form'''
    data_form = {
        'name': currrent_excercise.name,
        'desciption': currrent_excercise.description,
        'video_url': currrent_excercise.link_video,
        'listing_category': currrent_excercise.category,
        'duration': currrent_excercise.duration,
        'equipment': currrent_excercise.equipment,
        'listing_dificulty': currrent_excercise.dificulty
    }

    '''Admin Form code'''
    if request.method == "POST" and 'btn_approve' in request.POST:
        Exercise.objects.filter(id=exercise_id).update(approved = True)
    elif request.method == "POST" and 'btn_delete' in request.POST:
        Exercise.objects.get(id=exercise_id).delete()
        return render(request, "excercise/explore.html", {
            "items": Exercise.objects.filter(approved=True),
            "items_review": Exercise.objects.filter(approved=False)
        })
    elif request.method == "POST" and 'btn_submit' in request.POST:
        formRequest = RequestExerciseForm(request.POST)
        if formRequest.is_valid():
            p_name = formRequest.cleaned_data["name"]
            p_desciption = formRequest.cleaned_data["desciption"]
            p_video_url = formRequest.cleaned_data["video_url"]
            p_listing_category = formRequest.cleaned_data["listing_category"]
            p_duration = formRequest.cleaned_data["duration"]
            p_equipment = formRequest.cleaned_data["equipment"]
            p_listing_dificulty = formRequest.cleaned_data["listing_dificulty"]

            Exercise.objects.filter(id=exercise_id).update(name = p_name, description = p_desciption, link_video = p_video_url, category = p_listing_category, duration = p_duration, equipment = p_equipment, dificulty = p_listing_dificulty, approved = True)

    if request.user.is_authenticated:
        routineResultSet = Routine.objects.filter(user_id=request.user)
    else:
        routineResultSet = None
    
    return render(request, "excercise/exercise_detail.html", {
            "exercise": Exercise.objects.get(id=exercise_id),
            "routines": routineResultSet,
            "editExerciseForm":RequestExerciseForm(data_form)
        })


def create_routine(request):  
    return render(request, "excercise/create_routine.html")


def edit_routine(request):
    new_position = 1            

    form  = AddExerciseRoutine(request.POST)    
    if form.is_valid():
        print(sys.stderr, "Routine Name: ", form.cleaned_data["slc_routine"])
        current_routine = Routine.objects.get(name=form.cleaned_data["slc_routine"], user_id=request.user)
        list_exercise = RoutineExcercise.objects.filter(routine_id=current_routine).order_by('position')
        list_exercises = []
        list_exercises_aux = []
        auxRoutineRDay_list = []
        auxRoutineDaysDataDic = {}
        
        #Get all the exercises related with selected routine
        for iter in list_exercise:
            list_exercises.append(iter.excercise_id)
        
        # Using the aux class
        for iter in list_exercise:
            new_aux = AuxExecisePosition(iter.excercise_id,iter)
            list_exercises_aux.append(new_aux)
        last_position = list_exercise.last()
        if last_position != None:
                new_position = last_position.position + 1
        
        # Setting up the routine form
        list_routine_days = RoutineDay.objects.filter(routine_id = current_routine)
        auxRoutineRDay =  AuxRoutineRDay(current_routine, list_routine_days)
        
        for iter in list_routine_days:
            auxRoutineRDay_list.append({'day': iter.day_of_week, 'hour': iter.start_hour})
            
        auxRoutineDaysDataDic = {
            'data': auxRoutineRDay_list
        }
        #       Transforming the days data on JSON to get processed by JS on the front
        auxRoutineDaysDataDic = dumps(auxRoutineDaysDataDic)
        if request.method == "POST" and 'btn_add' in request.POST:
            form  = AddExerciseRoutine(request.POST)
            if form.is_valid():
                current_exercise = Exercise.objects.get(id=form.cleaned_data["id_exercise"])
                
                # Creating the new RoutineExercise
                new_routine_excercise = RoutineExcercise(position = new_position, routine_id = current_routine, excercise_id = current_exercise)
                new_routine_excercise.save()
                new_routine_excercise_aux = AuxExecisePosition(new_routine_excercise.excercise_id,new_routine_excercise)
                list_exercises_aux.append(new_routine_excercise_aux)
                
                print(sys.stderr, "Updating the routine duration: ")
                setRoutineDuration(current_routine.id)
                print(sys.stderr, "Fininshing the duration update")
                
                
                return render(request, "excercise/edit_routine.html", {
                    "exercises":list_exercises,
                    "aux_exercises":list_exercises_aux,
                    "aux_routine_days": auxRoutineRDay,
                    'aux_days_js':  auxRoutineDaysDataDic
                })
    
    return render(request, "excercise/edit_routine.html",{
        "exercises":list_exercises,
        "aux_exercises":list_exercises_aux,
        "aux_routine_days": auxRoutineRDay,
        'aux_days_js':  auxRoutineDaysDataDic
    })

'''AUX functions'''

def setRoutineDuration(routine_id):
    print(sys.stderr, "Updating total time routine")
    total_duration = 0
    '''Get the routine'''
    
    current_routine = Routine.objects.get(id = routine_id)
    
    '''Get all the exercises'''
    
    exercises = RoutineExcercise.objects.filter(routine_id = current_routine)
    for iter in exercises:
        aux_repetitions = iter.repetitions
        current_exercise = iter.excercise_id
        aux_duration = current_exercise.duration
        total_duration = total_duration + (aux_duration * aux_repetitions)
    
    current_routine.duration = total_duration
    current_routine.save()
    print(sys.stderr, "Finishing total time routine")
    
def calEndHour(start_hour, p_minutes):
    
    print(sys.stderr, "Start hour: ", start_hour, " Minutes: ", p_minutes)
    
    start_hour_tra = datetime.datetime.strptime(start_hour, '%H:%M')
    result = start_hour_tra + datetime.timedelta(minutes=int(p_minutes))
    
    print(sys.stderr, "Result: ", result)
    
    return str(result.time())[:-3]
    

'''RESPONSE API'''

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List':'/list_exercise_routine/<int:pk>/',
        'UpdatePosition':'/update_exercise_routine_position/<int:pk>/',
        'UpdateRepetition':'/update_exercise_routine_repetition/<int:pk>/',
        'Delete':'/delete_exercise_routine/<int:pk>/'
    }
    return Response(api_urls)

@api_view(['GET'])
def apiList(request, pk):
    
    list_exercise = RoutineExcercise.objects.filter(routine_id=pk).order_by('position')
    list_exercises_aux = []
    
    for iter in list_exercise:
        new_aux = AuxExecisePosition(iter.excercise_id,iter)
        list_exercises_aux.append(new_aux)
    
    new_aux_json = AuxSerializableExecisePosition(list_exercises_aux)
        
    json_data = json.dumps(new_aux_json.__dict__, default=lambda o: o.__dict__, indent=4)
    
    return Response(json_data)

@api_view(['POST'])
def apiUpdatePosition(request, pk):
    print(sys.stderr, "Updating exerciseRoutine on backend")    
    
    old_position = request.data["old_position"]
    new_position = request.data["new_position"]
        
    RoutineExcercise.objects.filter(position = new_position).update(position = int(old_position))
    RoutineExcercise.objects.filter(id = pk).update(position = int(new_position))
        
    return Response('Exercises updated')

@api_view(['POST'])
def apiUpdateRepetitions(request, pk):
    print(sys.stderr, "Updating exerciseRoutine on backend")    
    
    current = RoutineExcercise.objects.get(id=pk)
    serializer = RoutineExcerciseSerializer(instance=current, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
    else:
        print(sys.stderr, "Error: Serializer invalid")
    setRoutineDuration(current.routine_id.id)
    return Response(serializer.data)

@api_view(['DELETE'])
def apiDelete(request, pk):
    
    auxRoutineExcercise = RoutineExcercise.objects.get(id = pk)
    auxRoutine = auxRoutineExcercise.routine_id
    
    '''Update all the lowest position'''
    massiveUpdate = RoutineExcercise.objects.filter(position__gt=auxRoutineExcercise.position)
    for iter in massiveUpdate:
        RoutineExcercise.objects.filter(id=iter.id).update(position = iter.position - 1)
    
    auxRoutineExcercise.delete()
    
    setRoutineDuration(auxRoutine.id)
    
    return Response('RoutineExcercise Deleted')
