from django.contrib import admin

# Register your models here.

from .models import Listing, User, Bid, Comment, Watchlist

admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)