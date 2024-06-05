
import logging
import json
import timeit

from openai import OpenAI
from django.conf import settings

from gpt_query_client.client import GPTQueryClient

logger = logging.getLogger(__name__)


class OpenAIQueryClient(GPTQueryClient):

    def __init__(self, gpt_service=None, gpt_model_name=None, max_tokens=None, model_temperature=None, top_p=None):
        self.gpt_service = gpt_service
        self.gpt_model_name = gpt_model_name
        self.max_tokens = max_tokens
        self.model_temperature = model_temperature
        self.top_p = top_p

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
        )
        self.messages = [
            {
                "role": "system",
                "content":  "You are a helpful assistant helping a user plan a trip. "
                            "The user has provided the following information to generate a "
                            "travel itinerary:"
            }
        ]

    def _generate_prompt(self, data):
        """
        """
        city = data.get("city")
        country = data.get("country")
        no_of_days = data.get("no_of_days")
        month = data.get("month")
        food_preference = data.get("food_pref")
        accommodation_preference = data.get("accomodation_pref")
        traveling_with_preference = data.get("travelling_with_pref")
        traveling_style_preference = data.get("travelling_style_pref")
        custom_requirements = data.get("custom_requirements")

        prompt = f"""
            Generate a detailed travel itinerary for a trip. The inputs are:

            City: {city}
            Country: {country}
            Number of Days: {no_of_days}
            Month: {month}
            Food Preference to be included in itinerary: {food_preference}
            Accommodation Preference to be included in itinerary: {accommodation_preference}
            Traveling With: {traveling_with_preference}, curate the itinerary accordingly.
            Traveling Style: {traveling_style_preference}, curate the itinerary accordingly.
            Custom Requirement: {custom_requirements}

            Divide each day into morning, afternoon, and evening. Also, please curate the itinerary according to
            any custom requirements provided by the user as well.
            The output should be in JSON format, structured as follows:

            {{
                "data_day_wise": {{
                    "day_1": {{
                        "name": "Day 1",
                        "body": "A description of the day's activities and highlights.",
                        "experiences_and_activities": [
                            "List of activities and experiences planned for the day."
                        ],
                        "tips": [
                            "Travel tips or recommendations for the day."
                        ]
                    }},
                    // Continue for as many days as required
                }},
                "data_destination": {{
                    "name": "{city}, {country}",
                    "weather": "Current or typical weather conditions during the travel period provided by the user.",
                    "language": "Primary languages spoken at the destination.",
                    "currency": "Local currency and exchange rates.",
                    "essentials": [
                        "List of essential items to carry or be aware of."
                    ],
                    "official_tourism_websites": [
                        "List of official tourism websites for more information."
                    ]
                }}
            }}

            Provide a day-wise itinerary including activities, experiences, and travel tips. 
            Ensure the output is informative, engaging, and aligns with the provided preferences and 
            custom requirements.
            """
        return prompt

    def execute_query(self, data):
        prompt = self._generate_prompt(data)
        customer_id = data.get("customer_id")
        self.messages.append({"role": "user", "content": prompt})

        try:
            st = timeit.timeit()
            logger.info(f"Executing query to OpenAI API: prompt: {prompt}, "
                        f"customer_id: {customer_id}, model: {self.gpt_model_name},"
                        f" max_tokens: {self.max_tokens}, temperature: {self.model_temperature},"
                        f" top_p: {self.top_p}")
            completion = self.client.chat.completions.create(
                model=self.gpt_model_name,
                messages=self.messages,
                user=str(customer_id),
                max_tokens=self.max_tokens,
                temperature=self.model_temperature,
                top_p=self.top_p,
            )
            response_content = completion.choices[0].message.content
            response_dict = json.loads(response_content.replace("```json", "").replace("```", ""))
            self.messages.append({"role": "assistant", "content": response_content})
            et = timeit.timeit()
            logger.info(f"Query to OpenAI API completed in {et - st} seconds. Response: {response_dict}")
            return response_dict
        except Exception as e:
            logger.error(f"Error executing query to OPEN AI API: {e}")
            raise

    def modify_itinerary(self, modification_request, customer_id):
        self.messages.append({"role": "user", "content": modification_request})

        try:
            completion = self.client.chat.completions.create(
                model=self.gpt_model_name,
                messages=self.messages,
                user=str(customer_id),
                max_tokens=self.max_tokens,
                temperature=self.model_temperature,
                top_p=self.top_p,
            )
            response_content = completion.choices[0].message['content']
            self.messages.append({"role": "assistant", "content": response_content})
            response_dict = json.loads(response_content.replace("```json", "").replace("```", ""))
            return response_dict
        except Exception as e:
            logger.error(f"Error executing query to OpenAI API: {e}")
            raise
