from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField()
    image = models.URLField()
    category = models.CharField(max_length=64)
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

class Reply(models.Model):
    text = models.TextField()
    likes = models.PositiveIntegerField()
    comment = ForeignKey("Comment", on_delete=CASCADE, related_name="replies")
