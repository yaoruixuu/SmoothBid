from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"

class Bid(models.Model):
    val = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")
    
    def __str__(self):
        return f"{self.user} {self.val}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    img_url = models.CharField(max_length=400, blank=True)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="listing", blank=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")
    category = models.CharField(max_length=64, blank=True, null=True)
    active = models.BooleanField()
    
    def __str__(self):
        return f"{self.title}"
    
class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment" ,null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment")
    
    def __str__(self):
        return f"{self.user.username}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    item = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name="watchlist")

    def __str__(self):
        return self.user.username+" "+self.item.title
    