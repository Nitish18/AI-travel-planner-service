
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from karo_travel_plan.services.travel_itinerary_service import TravelItineraryService


logger = logging.getLogger(__name__)


class AllTravelItinerariesView(APIView):

    def get(self, request):
        """
        Get all travel itineraries
        """

        # Access query parameters
        customer_id = request.GET.get('customer_id')
        city = request.GET.get('city')
        country = request.GET.get('country')
        month = request.GET.get('month')
        food_pref = request.GET.get('food_pref')
        accomodation_pref = request.GET.get('accomodation_pref')
        travelling_with_pref = request.GET.get('travelling_with_pref')
        travelling_style_pref = request.GET.get('travelling_style_pref')

        travel_itineraries = TravelItineraryService.get_all_travel_itineraries(
            customer_id=customer_id,
            city=city,
            country=country,
            month=month,
            food_pref=food_pref,
            accomodation_pref=accomodation_pref,
            travelling_with_pref=travelling_with_pref,
            travelling_style_pref=travelling_style_pref,
        )

        return Response(travel_itineraries, status=status.HTTP_200_OK)


    def post(self, request):
        """
        Create a new travel itinerary

        response schema: {
            'itiniary_id': "uuid",
            'data_day_wise': {
                'day_id(uuid)': {
                    'name': "Day 1",
                    'body': "",
                    'experiences_and_activities': [],
                    'tips': [],
                },
            },
            'data_destination': {
                'name': "",
                'weather': "",
                'language': "",
                'currency': "",
                'essentials': [],
                'official_tourism_websites': [],
                'taxi_services': [],
            },
            'data_hotel': [],
            'data_flight': [],
            'data_food_places': [],
        }

        """

        data = request.data
        error, res = TravelItineraryService.create_travel_itinerary(data)
        if error:
            return Response({"error": res},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(res, status=status.HTTP_201_CREATED)


class TravelItineraryView(APIView):

    def get(self, request, itinerary_id):
        """
        Get travel itinerary by id
        """

        res = TravelItineraryService.get_travel_itinerary_by_id(itinerary_id)
        if not res:
            return Response({"error": "Travel itinerary not found"},
                            status=status.HTTP_404_NOT_FOUND)
        return Response(res, status=status.HTTP_200_OK)

    def put(self, request, itinerary_id):
        """
        Update travel itinerary by id
        """

        payload = request.data

        travel_itinerary = TravelItineraryService.get_travel_itinerary_by_id(itinerary_id)
        if not travel_itinerary:
            return Response({"error": "Travel itinerary not found"},
                            status=status.HTTP_404_NOT_FOUND)
        res = TravelItineraryService.update_travel_itinerary(itinerary_id, payload)
        if not res:
            return Response({"error": res},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(res, status=status.HTTP_200_OK)


    def patch(self, request, itinerary_id):
        """
        Partially update travel itinerary by id. For now, we are supporting day wise info update.
        """

        payload = request.data
        travel_itinerary = TravelItineraryService.get_travel_itinerary_by_id(itinerary_id)
        if not travel_itinerary:
            return Response({"error": "Travel itinerary not found"},
                            status=status.HTTP_404_NOT_FOUND)

        res = TravelItineraryService.update_travel_itinerary_day_wise_info_by_id(itinerary_id, payload)
        if not res:
            return Response({"error": res},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(res, status=status.HTTP_200_OK)

    def delete(self, request, itinerary_id):
        """
        Delete travel itinerary by id
        """

        res = TravelItineraryService.delete_travel_itinerary_by_id(itinerary_id)
        if not res:
            return Response({"error": res},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(res, status=status.HTTP_200_OK)
