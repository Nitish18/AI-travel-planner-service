# karo_travel_plan/urls.py
from django.urls import path

from karo_travel_plan.views import AllTravelItinerariesView, TravelItineraryView


urlpatterns = [
    path('itineraries/', AllTravelItinerariesView.as_view(), name='all_travel_itineraries'),
    path('itinerary/<str:itinerary_id>/', TravelItineraryView.as_view(), name='travel_itinerary'),
]
