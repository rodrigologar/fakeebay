from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import forms
from . import models


def index(request):
    
    listings = models.Listing.objects.all()
    
    return render(request, "auctions/index.html", {
        "listings": listings
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
            user = models.User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "auctions/register.html")
    

@login_required(login_url='/login')
def create_listing(request):
    if request.method == 'POST':
        form = forms.ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.lister = request.user
            listing.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            message = 'Invalid Listing'
            return render(request, "auctions/create_listing.html", {
                'form': form,
                'message': message
            })
            
    form = forms.ListingForm()
    
    return render(request, "auctions/create_listing.html", {
        'form': form
    })
    

def listing(request, listing_id):
    listing = models.Listing.objects.get(id=listing_id)
    button_value = "Add to Watchlist"
    bids = models.Bid.objects.filter(listing=listing)
    comments = reversed(models.Comment.objects.filter(listing=listing))

    if request.method == 'POST':
        if 'watchlist' in request.POST:
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('login_view'))
            
            check = models.WatchlistedListing.objects.filter(user=request.user, listing=listing)
            
            if check:
                watchlist = models.WatchlistedListing.objects.get(user=request.user, listing=listing)
                watchlist.delete()
                
                return HttpResponseRedirect(reverse('index'))
            else:
                watchlist = models.WatchlistedListing(user=request.user, listing=listing)
                watchlist.save()
            
                return HttpResponseRedirect(reverse('watchlist', args=[request.user.id]))
        
        elif 'place_bid' in request.POST:
            bidded_price = request.POST['bid']
            
            bid = models.Bid(listing=listing, bidded_price=bidded_price, bidder=request.user)
            bid.save()
            return HttpResponseRedirect(reverse('listing', args=[listing.id]))
        
        elif 'close_auction' in request.POST:
            listing.is_open = False
            listing.save()
            
            return HttpResponseRedirect(reverse('listing', args=[listing.id]))
        
        elif 'post_comment' in request.POST:
            comment_text = request.POST['comment_text']
            
            comment = models.Comment(text=comment_text, commenter=request.user, listing=listing)
            comment.save()
            
            return HttpResponseRedirect(reverse('listing', args=[listing.id]))
    
    if request.user.is_authenticated:
        check = models.WatchlistedListing.objects.filter(user=request.user, listing=listing)
        
        if check:
            button_value = "Remove from Watchlist"
    
    categories = dict(models.CATEGORIES)
    
    if not listing.category:
        category = "Not Listed"
    else:
        category = categories[listing.category]
        
    current_bid = ''
    current_bidder = ''
    
    if bids:
        current_bid = bids.last()
        current_bidder = current_bid.bidder.username
    
    return render(request, "auctions/listing.html", {
        'listing': listing,
        'category': category,
        'button_value': button_value,
        'current_bid': current_bid,
        'current_bidder': current_bidder,
        'comments': comments
    })
    
@login_required(login_url='/login')
def watchlist(request, user_id):
    watchlist = models.WatchlistedListing.objects.filter(user=user_id)
        
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })
    
def categories(request):
    categories = models.CATEGORIES
    
    return render(request, "auctions/categories.html", {
        "categories": categories
    })
    
def results(request, category):
    listings = models.Listing.objects.filter(category=category)
    
    return render(request, "auctions/results.html", {
        "listings": listings
    })
