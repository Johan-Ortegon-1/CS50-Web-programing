from datetime import date
import sys
from webbrowser import get
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse

import datetime
import time
import logging

from .models import *


def index(request):
    print(sys.stderr, "Insede Index function")
    message = None
    if request.method == "POST" and 'create_post' in request.POST:
        postContent = request.POST.get('post_content')
        if postContent == None or postContent == "":
            message = "You can't create an empty post."
        else:
            p_user_id = request.user
            t = time.localtime()
            current_time = time.strftime("%H:%M", t)
            p_date = str(datetime.date.today()) + " " + current_time
            new_post = Post(content=postContent,
                            created_by=p_user_id, date=p_date)
            new_post.save()
    elif request.method == "POST" and 'edit_post' in request.POST:
        postContent = request.POST.get('text_area_edit_post')
        print(sys.stderr, "Content: ", postContent)
        if postContent != None and postContent != "":
            post_id = request.POST.get('id_post')
            print(sys.stderr, "ID: ", post_id)
            current_post = Post.objects.get(id=post_id)
            current_post.content = postContent
            current_post.save()
        return render(request,"network/index.html")
    elif request.method == "POST" and 'btn_like_dislike' in request.POST:
        post_id = request.POST.get('id_post')
        try:
            p_current_post = Post.objects.get(id=post_id)
        except p_current_post.DoesNotExist:
            raise Http404("Post not found.")
        
        '''User is performing a dislike(if) or like(else)'''
        if Like.objects.filter(user_id=request.user, post_id=p_current_post).exists():
            print(sys.stderr, "a dislike is comming")
            Like.objects.filter(user_id=request.user, post_id=p_current_post).delete()
            p_current_post.like_counter = p_current_post.like_counter - 1
            p_current_post.save()
            return JsonResponse({'flag':'dislike'})
            '''return flag to front asinc function in AJAX to decerase the counter'''
        else:
            print(sys.stderr, "a like is comming")
            new_like = Like(user_id=request.user, post_id=p_current_post)
            new_like.save()
            p_current_post.like_counter = p_current_post.like_counter + 1
            p_current_post.save()
            return JsonResponse({'flag':'like'})
            '''return flag to front asinc function in AJAX to increase the counter'''
        
    page_obj = setUpPaginator(request, Post.objects.order_by('-date').all())

    return render(request, "network/index.html", {
        "message": message,
        "page_obj": page_obj
    })


def following_posts(request):
    '''OR + Bandera'''
    message = None
    posts = None
    post_final = []
    try:
        p_user_current = User.objects.get(id=request.user.id)
    except p_user_current.DoesNotExist:
        raise Http404("User not found.")
    
    posts = Post.objects.order_by('-date').all()
    posts_list = list(posts)
    for iter in posts_list:
        if Follow.objects.filter(follower=p_user_current, followed=iter.created_by).exists():
            post_final.append(iter)
    
    page_obj = setUpPaginator(request, post_final)
    return render(request, "network/index.html", {
        "message": message,
        "page_obj": page_obj
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, user_id):
    '''POST REQUEST HANDLER'''
    if request.method == "POST" and 'edit_post' in request.POST:
        print(sys.stderr, "Profile function")
        postContent = request.POST.get('text_area_edit_post')
        if postContent != None and postContent != "":
            post_id = request.POST.get('id_post')
            current_post = Post.objects.get(id=post_id)
            current_post.content = postContent
            current_post.save()
        return render(request,"network/index.html")
    
    try:
        p_user = User.objects.get(id=user_id)
        p_user_current = User.objects.get(id=request.user.id)
    except p_user.DoesNotExist or p_user_current.DoesNotExist:
        raise Http404("User not found.")
    
    if request.method == "POST" and 'follow' in request.POST:
        new_follower = Follow(follower = request.user, followed = p_user)
        new_follower.save()
        '''Updating the Followed'''
        p_user.followers_counter = p_user.followers_counter + 1
        p_user.save()
        '''Updating the Follower'''
        p_user_current.following_counter = p_user_current.following_counter + 1
        p_user_current.save()
        
    elif request.method == "POST" and 'unfollow' in request.POST:
        Follow.objects.get(follower = request.user, followed = p_user).delete()
        '''Updating the Followed'''
        p_user.followers_counter = p_user.followers_counter - 1
        p_user.save()
        '''Updating the Follower'''
        p_user_current.following_counter = p_user_current.following_counter - 1
        p_user_current.save()
    elif request.method == "POST" and 'btn_like_dislike' in request.POST:
        post_id = request.POST.get('id_post')
        try:
            p_current_post = Post.objects.get(id=post_id)
        except p_current_post.DoesNotExist:
            raise Http404("Post not found.")
        
        '''User is performing a dislike(if) or like(else)'''
        if Like.objects.filter(user_id=request.user, post_id=p_current_post).exists():
            print(sys.stderr, "a dislike is comming")
            Like.objects.filter(user_id=request.user, post_id=p_current_post).delete()
            p_current_post.like_counter = p_current_post.like_counter - 1
            p_current_post.save()
            return JsonResponse({'flag':'dislike'})
            '''return flag to front asinc function in AJAX to decerase the counter'''
        else:
            print(sys.stderr, "a like is comming")
            new_like = Like(user_id=request.user, post_id=p_current_post)
            new_like.save()
            p_current_post.like_counter = p_current_post.like_counter + 1
            p_current_post.save()
            return JsonResponse({'flag':'like'})
            '''return flag to front asinc function in AJAX to increase the counter'''

    '''PROCESS AND REQUEST THE CONTENT'''
    green_button = False
    red_button = False
    try:
        page_obj = setUpPaginator(request, Post.objects.filter(created_by=p_user).order_by('-date'))
    except Post.DoesNotExist:
        raise Http404("Posts not found.")

    '''Render the button'''
    current_user = request.user
    '''Condition 1. Is the same user → Dont display the button'''
    '''Condition 2. Is a different user & is not a follower → Displays green button'''
    '''Condition 3. Is a different user & is a follower → Displays red button'''
    if current_user != p_user:
        if Follow.objects.filter(follower=current_user, followed=p_user).exists():
            red_button = True
        else:
            green_button = True
            
    return render(request, "network/profile.html", {
        "p_user": p_user,
        "page_obj": page_obj,
        "green_button": green_button,
        "red_button": red_button
    })


''''Support functions'''
def setUpPaginator(request, resultSet):
    paginator = Paginator(resultSet, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj