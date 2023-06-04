from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_owner")
    highest_bid_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hihgest", null = True)
    img_url = models.CharField(max_length=1000)
    title = models.CharField(max_length=80, null=True)
    description = models.TextField()
    category = models.CharField(max_length=100, null = True)
    starting_bid = models.DecimalField(max_digits=13, decimal_places=2, null = True)
    current_price = models.DecimalField(max_digits=13, decimal_places=2, null = True)
    status = models.BooleanField(null = True)
    
class Bids(models.Model):
    amount = models.DecimalField(max_digits=13, decimal_places=2)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_owner")
    auction_id = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="auction_bid_related")

class Comment(models.Model):
    date = models.DateTimeField()
    content = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_owner")
    auction_id = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="auction_comment_related")
    
class WatchList(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watch_list_owner")
    auction_id = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="auction_watch_list_related")