from django.contrib import admin
from .models import User, AuctionListing, Bids, Comment, WatchList

# Register your models here.
admin.site.register(User)
admin.site.register(AuctionListing)
admin.site.register(Bids)
admin.site.register(Comment)
admin.site.register(WatchList)

