from django.core.cache import cache
from .models import CarAd  

def warm_cache():
    """
    Loads data from the database into the cache.
    """
    ads = CarAd.objects.all()  # Get all ads from the database
    for ad in ads:
        cache.set(ad.code, True, timeout=None)  # Add each ad's code to the cache