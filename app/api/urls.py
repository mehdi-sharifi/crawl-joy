from django.urls import path
from .views import *
from django.urls import path
from .views import PersonView, PersonDetailView, CarAdView, CarAdDetailView, CrawlView, SendNotificationView
urlpatterns =[]

person_api = [
    path('v1/persons/', PersonView.as_view()),
    path('v1/persons/<int:id>/', PersonDetailView.as_view()),
]

car_ads_api = [
    path('v1/car_ads/', CarAdView.as_view(), name='car_ads'),
    path('v1/car_ads/<str:id>/', CarAdDetailView.as_view(), name='car_ad_detail'),
]

crawl_api = [
    path('v1/crawl/', CrawlView.as_view(), name='crawl'),
]

notification_api = [
    path('v1/sendnotification/', SendNotificationView.as_view(), name='sendnotification'),
 
]

urlpatterns.extend(person_api)
urlpatterns.extend(car_ads_api)
urlpatterns.extend(crawl_api)
urlpatterns.extend(notification_api)