from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, SET_DEFAULT, SET_NULL
from django.db.models.fields.related import ForeignKey


class User(AbstractUser):
    pass

CATEGORIES = [
    ('AU', 'Automotive'),
    ('BA', 'Babies'),
    ('BE', 'Beauty'),
    ('BO', 'Books'),
    ('EL', 'Electronics'),
    ('FA', 'Fashion'),
    ('HE', 'Health'),
    ('HO', 'Home'),
    ('SP', 'Sports'),
    ('OT', 'Other')
]

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField()
    image = models.URLField(blank=True)
    category = models.CharField(max_length=2, choices=CATEGORIES, blank=True)
    lister = models.ForeignKey("User", on_delete=models.CASCADE, related_name="listings")
    date = models.DateTimeField(auto_now_add=True)
    is_open = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.id}: {self.title} from user {self.lister.id}"
    
class Bid(models.Model):
    listing = models.ForeignKey("Listing", on_delete=CASCADE, related_name="bids")
    bidded_price = models.PositiveIntegerField()
    bidder = models.ForeignKey("User", on_delete=CASCADE, related_name="bids")
    date = models.DateTimeField(auto_now_add=True)
    
class Comment(models.Model):
    text = models.TextField()
    likes = models.PositiveIntegerField()
    commenter = models.ForeignKey("User", on_delete=CASCADE, related_name="comments")

class Reply(models.Model):
    text = models.TextField()
    likes = models.PositiveIntegerField()
    replier = models.ForeignKey("User", on_delete=CASCADE, related_name="user_replies")
    comment = ForeignKey("Comment", on_delete=CASCADE, related_name="comment_replies")
    
class WatchlistedListing(models.Model):
    user = models.ForeignKey("User", on_delete=CASCADE)
    listing = models.ForeignKey("Listing", on_delete=CASCADE)
    
    def __str__(self):
        return f"Watchlisted by {self.user.id}: {self.listing.title}"
