
import logging
import uuid
from typing import Optional

from django.db import transaction

from karo_travel_plan.models import TravelPlanQuery, TravelPlanQueryResponse
from karo_travel_plan.providers.customer import get_customer_from_id
from karo_travel_plan.helpers import is_customer_allowed
from gpt_query_client.gpt_models.openai_model import OpenAIQueryClient

logger = logging.getLogger(__name__)


class TravelItineraryService:

    @staticmethod
    def get_all_travel_itineraries(customer_id = None, city = "", country = "", month = "", food_pref = "",
                                   accomodation_pref = "", travelling_with_pref = "", travelling_style_pref = "",
                                   is_active=True):
        data = []
        travel_itineraries = TravelPlanQueryResponse.objects.filter(is_active=is_active)
        if customer_id:
            travel_itineraries = travel_itineraries.filter(travel_plan_query__customer_id=customer_id)
        if city:
            travel_itineraries = travel_itineraries.filter(travel_plan_query__city=city)
        if country:
            travel_itineraries = travel_itineraries.filter(travel_plan_query__country=country)
        if month:
            travel_itineraries = travel_itineraries.filter(travel_plan_query__month=month)
        if food_pref:
            travel_itineraries = travel_itineraries.filter(travel_plan_query__food_pref=food_pref)
        if accomodation_pref:
            travel_itineraries = travel_itineraries.filter(travel_plan_query__accomodation_pref=accomodation_pref)
        if travelling_with_pref:
            travel_itineraries = travel_itineraries.filter(travel_plan_query__travelling_with_pref=travelling_with_pref)
        if travelling_style_pref:
            travel_itineraries = travel_itineraries.filter(
                travel_plan_query__travelling_style_pref=travelling_style_pref
        )
        for travel_plan_query_response_obj in travel_itineraries:
            data.append(TravelItineraryService._format_travel_itinerary_data(travel_plan_query_response_obj))

        return data

    @staticmethod
    def create_travel_itinerary(data = None) -> tuple:
        """
        Create Travel Itinerary

        data schema: {
            'customer_id': "",
            'city': "",
            'country': "",
            'month': "",
            'no_of_days': "",
            'food_pref': "",
            'accomodation_pref': "",
            'travelling_with_pref': "",
            'travelling_style_pref': "",
            'custom_requirements': "",
        }

        """

        res = {}

        customer = get_customer_from_id(data.get("customer_id"))
        if not is_customer_allowed(customer):
            error_msg = f"Customer with id {data.get('customer_id')} is not allowed to create travel itinerary"
            logger.info(error_msg)
            return (True, error_msg)

        # fetching query response from cache first if available
        # TODO: implement cache

        # initialize GPT client
        gpt_client_config = customer.plan.gpt_service_type_config

        try:
            gpt_client = TravelItineraryService._initialize_gpt_client(gpt_client_config)
            gpt_res = gpt_client.execute_query(data)
            res['data_day_wise'] = TravelItineraryService._format_gpt_data(gpt_res['data_day_wise'])
            res['data_destination'] = gpt_res['data_destination']
        except Exception as e:
            error_msg = f"Error while creating travel itinerary from GPT: {e}"
            logger.error(error_msg)
            return (True, error_msg)

        # fetch data from other services like hotel, flight, food places, etc
        # TODO implement other services
        res['data_hotel'] = []
        res['data_flight'] = []
        res['data_food_places'] = []

        # save query response to db
        try:
            with transaction.atomic():
                travel_plan_query_uuid = uuid.uuid4()
                travel_plan_query_response_uuid = uuid.uuid4()
                travel_plan_query = TravelPlanQuery.objects.create(
                    id=travel_plan_query_uuid,
                    customer=customer,
                    no_of_days=data.get("no_of_days"),
                    city=data.get("city"),
                    country=data.get("country"),
                    month=data.get("month"),
                    food_pref=data.get("food_pref"),
                    accomodation_pref=data.get("accomodation_pref"),
                    travelling_with_pref=data.get("travelling_with_pref"),
                    travelling_style_pref=data.get("travelling_style_pref"),
                    custom_requirements=data.get("custom_requirements"),
                )
                logger.info(f"Travel itinerary query saved to db with id: {travel_plan_query.id}")
                travel_plan_query_res = TravelPlanQueryResponse.objects.create(
                    id=travel_plan_query_response_uuid,
                    travel_plan_query=travel_plan_query,
                    query_response_data=res,
                )
                logger.info(f"Travel itinerary saved to db with id: {travel_plan_query_res.id}")
                res['itinerary_id'] = travel_plan_query_res.id
        except Exception as e:
            error_msg = f"Error while saving travel itinerary to db: {e}"
            logger.error(error_msg)
            return (True, error_msg)

        return (False, res)

    @staticmethod
    def get_travel_itinerary_by_id(itininerary_id = None, is_active=True) -> Optional[dict]:
        travel_plan_query_response_obj = TravelPlanQueryResponse.objects.filter(id=itininerary_id,
                                                                                is_active=is_active).first()
        if not travel_plan_query_response_obj:
            return None
        return TravelItineraryService._format_travel_itinerary_data(travel_plan_query_response_obj)

    @staticmethod
    def update_travel_itinerary_by_id(itinerary_id = None, data = None) -> Optional[dict]:
        travel_itinerary = TravelPlanQueryResponse.objects.filter(id=itinerary_id).first()
        # update data
        travel_itinerary.query_response_data = data
        travel_itinerary.save()
        return TravelItineraryService._format_travel_itinerary_data(travel_itinerary)

    @staticmethod
    def update_travel_itinerary_day_wise_info_by_id(itinerary_id = None, data = None) -> Optional[dict]:
        travel_itinerary = TravelPlanQueryResponse.objects.filter(id=itinerary_id).first()

        # day wise data to be updated
        updated_day_wise_data = TravelItineraryService._updated_day_wise_data(
            travel_itinerary.query_response_data.get('data_day_wise'), data
        )

        data = travel_itinerary.query_response_data
        data['data_day_wise'] = updated_day_wise_data
        travel_itinerary.query_response_data = data
        travel_itinerary.save()
        return TravelItineraryService._format_travel_itinerary_data(travel_itinerary)

    @staticmethod
    def delete_travel_itinerary_by_id(itinerary_id = None) -> Optional[bool]:
        travel_itinerary = TravelPlanQueryResponse.objects.filter(id=itinerary_id).first()
        if not travel_itinerary:
            return None
        travel_itinerary.is_active = False
        travel_itinerary.save()
        return True

    @staticmethod
    def _format_travel_itinerary_data(travel_plan_query_response_obj = None):

        travel_plan_query = travel_plan_query_response_obj.travel_plan_query
        formatted_data = {
            "itinerary_id": travel_plan_query_response_obj.id,
            "customer_id": travel_plan_query.customer.id,
            "no_of_days": travel_plan_query.no_of_days,
            "city": travel_plan_query.city,
            "country": travel_plan_query.country,
            "month": travel_plan_query.month,
            "food_pref": travel_plan_query.food_pref,
            "accomodation_pref": travel_plan_query.accomodation_pref,
            "travelling_with_pref": travel_plan_query.travelling_with_pref,
            "travelling_style_pref": travel_plan_query.travelling_style_pref,
            "custom_requirements": travel_plan_query.custom_requirements,
            "data": travel_plan_query_response_obj.query_response_data,
            "updated_at": travel_plan_query_response_obj.updated_at,
            "created_at": travel_plan_query_response_obj.created_at,
            "upvote_count": travel_plan_query_response_obj.upvote_count,
        }
        return formatted_data

    @staticmethod
    def _initialize_gpt_client(config):
        if config.gpt_service == 'openai':
            return OpenAIQueryClient(
                gpt_service=config.gpt_service,
                gpt_model_name=config.gpt_model_name,
                max_tokens=config.max_tokens,
                model_temperature=config.model_temperature,
                top_p=config.top_p
            )
        else:
            raise ValueError("Unsupported GPT service")

    @staticmethod
    def _format_gpt_data(data=None) -> dict:
        formatted_data = {}
        for day_id, data_day in data.items():
            new_day_id = day_id + '_' + str(uuid.uuid4())
            formatted_data[new_day_id] = data_day
        return formatted_data

    @staticmethod
    def _updated_day_wise_data(current_day_wise_data, updated_day_wise_data):
        data = current_day_wise_data
        for day_id, day_data in updated_day_wise_data.items():
            data[day_id] = day_data
        return data
