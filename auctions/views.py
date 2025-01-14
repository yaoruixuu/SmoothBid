from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Watchlist


def index(request):
    category_set=set({})
    all_listings=Listing.objects.all()
    for item in all_listings:
        category_set.add(item.category)

    # one to one dicitonary
    dict = {}
    for category in category_set:
        lst_all=Listing.objects.filter(category=category, active=True)
        dict[category]=lst_all[:5]
    
   
    return render(request, "auctions/index.html",{
        "dict":dict
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

def categories(request):
    category_set=set({})
    all_listings=Listing.objects.all()
    for item in all_listings:
        category_set.add(item.category)

    # one to one dicitonary
    dict = {}
    for category in category_set:
        dict[category]=Listing.objects.filter(category=category).first()
    
    return render(request,"auctions/categories.html", {
         "dict":dict
    })

def categories_listings(request, category):
    category_set=set({})
    all_listings=Listing.objects.all()
    for item in all_listings:
        category_set.add(item.category)
    
    dict={}

    for cat in category_set:
        dict[cat]=[]
    
    for listing in all_listings:
        dict[listing.category].append(listing)


    return render(request,"auctions/categories_listing.html", {
        "categories_listings":dict[category], "category": category
    })


def create_listing(request, user):
    if request.method=="POST":
        title = request.POST["title"]
        starting_price = request.POST["starting_bid"]
        description = request.POST["description"]
        img_url = request.POST.get("img_url")
        categories = request.POST.get("category")

        try:
            starting_bid = Bid(val = float(starting_price), user=User.objects.get(username=user))
            starting_bid.save()
            listing = Listing(title=title, description=description, starting_bid=float(starting_price), bid = starting_bid, img_url=img_url, user=User.objects.get(username=user), category = categories, active=True)
            listing.save()
            listings=Listing.objects.all()

            return HttpResponseRedirect(reverse('index'))
       
        except:
            return render(request, "auctions/create_listing.html", {
                    "invalid":"Please enter a numerical value"})

        
    return render(request, "auctions/create_listing.html", {
        
    })


def listing(request, listing, user):

    requested_listing = Listing.objects.get(title=listing)

    add = True

    
    if request.method!='POST':
        try: 
            a = Watchlist.objects.get(user=User.objects.get(username=user), item=Listing.objects.get(title=listing))
            add=False
        
        except:
            add=True

    if request.method=='POST' and request.POST.get("close")!=None:
        obj = Listing.objects.get(title=listing)
        obj.active=False
        obj.save()
          

    if request.method=='POST' and request.POST.get("remove_listing")!=None:
        remove_watchlist_id = request.POST["remove_listing"]
        remove_listing = Watchlist.objects.filter(item=remove_watchlist_id, user=User.objects.get(username=user)).first()
        if remove_listing != None:
            remove_listing.delete()
        
        
    
    elif request.method=='POST' and request.POST.get("add_listing")!=None:
        add_watchlist_id = request.POST.get("add_listing")
        watchlist = Watchlist(user=User.objects.get(id=request.POST.get('user_id')), item=Listing.objects.get(id=add_watchlist_id))
        watchlist.save()
        add=False

    elif request.method=='POST' and request.POST.get('bid_amount')!=None:
        
        this_bid = request.POST.get('bid_amount')
        try:
            float(this_bid)
        except:
            return render(request, "auctions/listing.html",{
                "listing":requested_listing, "add_button":add, "error_msg":"Please enter a numerical value."
            })
        
        listing_bid=Listing.objects.get(title=listing).starting_bid
        if float(this_bid)<=listing_bid:
            return render(request, "auctions/listing.html",{
                "listing":requested_listing, "add_button":add, "error_msg":"Bid is below current bid value."
            })
        else:
            obj=Listing.objects.get(title=listing).bid
            obj.val=float(this_bid)
            obj.user=User.objects.get(username=user)
            obj.save()

    # create comment
    elif request.method=='POST' and request.POST.get('user_comment')!=None:
        user = User.objects.get(username=request.POST.get("user"))
        comment = request.POST.get("user_comment")
        obj = Comment(user=user, comment=comment, listing=Listing.objects.get(title=listing))
        obj.save()

    # getting comments
    try:
        listing_comments = Comment.objects.filter(listing=Listing.objects.get(title=listing))
    except:
        listing_comments=[]
    
   
    # getting highest bidder
    highest_bidder = Listing.objects.get(title=listing).bid.user

  
    # fetching requested listing again
    requested_listing = Listing.objects.get(title=listing)

    close=False
    if user!="AnonymousUser":
        if Listing.objects.get(title=listing).user == User.objects.get(username=user):
            if Listing.objects.get(title=listing).active:
                close=True


    return render(request, "auctions/listing.html", {
        "listing":requested_listing, "add_button":add, "close":close, "highest_bidder":highest_bidder, "comments":listing_comments
    })

def watchlist(request, user):
    user = User.objects.get(username=user)
    user_watchlist = Watchlist.objects.filter(user=user.id)
    items = []
    for watchlist_item in user_watchlist:

        if not Listing.objects.get(title=watchlist_item.item.title).active:
            remove = Watchlist.objects.get(item=Listing.objects.get(title=watchlist_item.item.title))
            remove.delete()

        else:
            items.append(watchlist_item.item)

    return render(request, "auctions/watchlist.html", {
        "listings":items
    })

