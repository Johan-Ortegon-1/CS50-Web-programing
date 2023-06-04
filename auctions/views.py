from random import choices
import sys
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
import datetime
import time

from .models import User, AuctionListing, Bids, Comment, WatchList

CATEGORY_OPTIONS = [
    ('vehicle','Vehicle'),
    ('technology','Technology'),
    ('home & forniture','Home & Forniture'),
    ('sport & fitness','Sport & Fitness'),
    ('tools','Tools'),
    ('entrertainment','Entertainment'),
    ('other', 'Other')
]

class CreateListingForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    desciption = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    img_url = forms.URLField(widget=forms.URLInput(attrs={'class':'form-control'}), required=False)
    listing_category = forms.CharField(widget=forms.Select(attrs={'class':'form-control'}, choices = CATEGORY_OPTIONS), required=False)
    starting_bid = forms.DecimalField(max_digits = 13, decimal_places = 2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    

def index(request):
    # return render(request, "auctions/index.html")
    return render(request, "auctions/index.html", {
        "items": AuctionListing.objects.exclude(status=False).all()
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "POST":
        formCreate = CreateListingForm(request.POST)
        if formCreate.is_valid():
            p_title = formCreate.cleaned_data["title"]
            p_desciption = formCreate.cleaned_data["desciption"]
            p_img_url = formCreate.cleaned_data["img_url"]
            p_listing_category = formCreate.cleaned_data["listing_category"]
            p_starting_bid = formCreate.cleaned_data["starting_bid"]
            p_user_id = request.user
            
            auction_listing = AuctionListing(user_id = p_user_id, title = p_title, description = p_desciption, starting_bid = p_starting_bid, current_price = 0, status = True)

            if p_img_url != None:
                auction_listing.img_url = p_img_url
            if p_listing_category != None:
                auction_listing.category = p_listing_category
            elif (p_listing_category == None and p_img_url == None):
                return render(request, "auctions/create_listing.html", {
                    "message": "A image URL or/and category is required."
                })
            # Attempt to create new listing
            try:
                auction_listing.save()
            except IntegrityError:
                return render(request, "auctions/create_listing.html", {
                    "message": "Error creating the Item"
                })
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create_listing.html", {
                "message": "Invalid form"
            })
                
    return render(request, "auctions/create_listing.html", {"fromCreateListing":CreateListingForm()})


def auction_listing(request, auction_listing_id):   
    message = None
    winner_message = None
    loser_message = None
    
    '''SQL Queries'''
    
    try:
        p_auction_listing = AuctionListing.objects.get(id=auction_listing_id)
    except AuctionListing.DoesNotExist:
        raise Http404("Auction listing not found.")
    
    try:
        p_comments = Comment.objects.filter(auction_id=p_auction_listing)
    except AuctionListing.DoesNotExist:
        raise Http404("Auction listing not found.")
    
    '''Form code'''
    
    if request.method == "POST" and 'remove_from_watchlist' in request.POST:
        WatchList.objects.get(user_id = request.user, auction_id = p_auction_listing).delete()
        
    elif request.method == "POST" and 'add_to_watchlist' in request.POST:
        new_warchlist = WatchList(user_id = request.user, auction_id = p_auction_listing)
        new_warchlist.save()
    
    elif request.method == "POST" and 'make_a_bid' in request.POST:
        new_bid = request.POST['bid']
        new_bid = float(new_bid)
        if new_bid < p_auction_listing.starting_bid and p_auction_listing.current_price == 0:
            message = "Sorry, your bid must be at least equal or higher than the Starting Price"
        elif p_auction_listing.current_price > 0 and new_bid < p_auction_listing.current_price:
            message = "Sorry, your bid must be at least higher than the highest Current Price"
        else:
            p_auction_listing.current_price = new_bid
            p_auction_listing.highest_bid_user_id = request.user
            p_auction_listing.save()
            new_bid_db = Bids(amount = new_bid, user_id = request.user, auction_id = p_auction_listing)
            new_bid_db.save()
            message = "Congratulations, your bid was registered"
    
    elif request.method == "POST" and 'close_auction' in request.POST:
        p_auction_listing.status = False
        p_auction_listing.user_id = request.user
        p_auction_listing.save()
    
    elif request.method == "POST" and 'post_comment' in request.POST:
        t = time.localtime()
        current_time = time.strftime("%H:%M", t)
        
        p_content_new_comment = request.POST['msg']
        p_auction_id_new_comment = p_auction_listing
        p_date = str(datetime.date.today()) + " " + current_time
        new_comment = Comment(date = p_date, content = p_content_new_comment, user_id = request.user, auction_id = p_auction_id_new_comment)
        new_comment.save()
        
        
    '''close and Winner code'''
    if p_auction_listing.status == False and p_auction_listing.highest_bid_user_id == request.user:
        winner_message = "You Won this auction, Congratulations!"
    elif p_auction_listing.status == False and p_auction_listing.highest_bid_user_id != request.user:
        loser_message = "This auctions is close"
        
    is_in_watchlist = True
    if request.user.is_authenticated:
        try:
            result = WatchList.objects.get(user_id = request.user.id, auction_id = auction_listing_id)
        except WatchList.DoesNotExist:
            is_in_watchlist = False
            
    is_author = False
    if request.user.id == p_auction_listing.user_id.id:
        is_author = True
    
    return render(request, "auctions/auction_listing.html", {
        "message": message,
        "winner_message": winner_message,
        "loser_message": loser_message,
        "auction_listing": p_auction_listing,
        "comments": p_comments,
        "is_in_watchlist": is_in_watchlist,
        "is_author": is_author,
    })
    
def watchlist_view(request):
    return render(request, "auctions/watchlist.html", {
        "items": WatchList.objects.filter(user_id = request.user)
    })

def categories_view(request):
    categories = []
    for iter in CATEGORY_OPTIONS:
        categories.append(iter[0])
    return render(request, "auctions/categories.html", {
        "items": categories
    })

def specific_category(request, category):
    return render(request, "auctions/specific_category.html", {
        "category": category,
        "items": AuctionListing.objects.filter(category=category).exclude(status=False).all()
    })
    
    
'''print(sys.stderr, 'Goodbye, cruel world!' + str(type(CATEGORY_OPTIONS[0])))'''
