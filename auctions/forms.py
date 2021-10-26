from django.db.models import fields
from django.forms import ModelForm
from . import models


class ListingForm(ModelForm):
    class Meta:
        model = models.Listing
        fields = [
            'title', 
            'description', 
            'price', 
            'image', 
            'category'
        ]
        
        labels = {
            'price': 'Starting Price'
        }