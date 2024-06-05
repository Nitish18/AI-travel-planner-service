# TRAVEL PLANNER using genAI

Backend service for the Travel Planner app known as TripKaro. This service exposes
RESTful APIs for the clients to consume. Client takes inputs from users such as destination city, travelling style, travelling with, etc
and generate a day wise itinerary for the trip. The service uses genAI to generate the itinerary.

## Table of Contents

- [TripKaro](#project-name)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [License](#license)

## Features

- **Travel Inspiration:** suggest places to visit according to users preferences and travel style and requirements.
- **Travel Planning:** creates a day wise itinerary for the trip using some input parameters.
- **Sharing:** allows users to download the itinerary in pdf format and share it with others.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Nitish18/karoGPT.git
    ```
   
2. Make sure that you have MySQL installed in your system. If not, install it.

3. Create a new database in MySQL:
    ```sql
    CREATE DATABASE karogpt;
    ```
4. Create a new python virtual environment:
    ```sh
    virtualenv -p python3 venv
    ```

5. Activate the virtual environment:
    ```sh
    source venv/bin/activate
    ```
6. Change the directory to the project directory:
    ```sh
    cd karoGPT_backend
    ```
7. Create a new file named `.env` in the project directory and add the following environment variables:
    ```sh
    export DB_USER='your_db_username'
    export DB_PASSWORD='your_db_password'
    export DB_HOST='localhost'
    export DB_NAME='karogpt'
    export OPENAI_API_KEY='your_openai_api_key'
   ```
8. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

9. Run the following command to create the database tables:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
   ```   

10. Run the following command to start the server:
    ```
    python manage.py runserver
    ```
   
## Usage
List of API endpoints:

1. `http://localhost/karo_travel_plan/itineraries/` - POST request to create a new itinerary.
   - Request body:
     ```json
     {
            "customer_id": "",
            "city": "Manali",
            "country": "India",
            "no_of_days": "3",
            "food_pref": "veg",
            "accomodation_pref": "hostel",
            "travelling_with_pref": "solo",
            "travelling_style_pref": ["adventure", "outdoor", "nature"],
            "custom_requirements": "I want to do river rafting as well.",
            "month": "July"
     }
     ```
   - Response:
     ```json
     {
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
            'data_food_places': []
        }
     ```
2. `http://localhost/karo_travel_plan/itineraries/` - GET request to get all the itineraries.
   - Response:
   ```json
     [
         {
            "itinerary_id": "d675b60b-6a4e-427e-9d0c-535159beabd2",
        "customer_id": 1,
        "no_of_days": 3,
        "city": "Manali",
        "country": "India",
        "month": "July",
        "food_pref": "veg",
        "accomodation_pref": "hostel",
        "travelling_with_pref": "solo",
        "travelling_style_pref": [
            "adventure",
            "outdoor",
            "nature"
        ],
        "custom_requirements": "",
        "data": {
            "data_hotel": [],
            "data_flight": [],
            "data_day_wise": {
                "day_1_9a57ff1e-586e-43c9-9c84-fbc424559e03": {
                    "body": "Welcome to Manali! Start your adventure with a mix of nature and outdoor activities.",
                    "name": "Day 1",
                    "tips": [
                        "Wear comfortable shoes for walking.",
                        "Carry a light jacket as the weather can be unpredictable.",
                        "Stay hydrated and carry a water bottle."
                    ],
                    "experiences_and_activities": [
                        "Morning: Arrive in Manali and check into your hostel. Freshen up and have a hearty vegetarian breakfast.",
                        "Morning: Visit the Hadimba Temple, a beautiful and serene spot surrounded by cedar forests.",
                        "Afternoon: Head to the Solang Valley for some adventure sports like paragliding and zorbing.",
                        "Evening: Return to Manali and explore the local market. Enjoy a vegetarian dinner at a local restaurant."
                    ]
                },
                "day_2_b66c61fc-4b48-489a-93d4-b83c99f2543a": {
                    "body": "Immerse yourself in the natural beauty of Manali with a mix of trekking and sightseeing.",
                    "name": "Day 2",
                    "tips": [
                        "Carry a small backpack with essentials like water, snacks, and a first-aid kit.",
                        "Wear comfortable trekking shoes.",
                        "Respect the local culture and environment."
                    ],
                    "experiences_and_activities": [
                        "Morning: Have breakfast at the hostel and prepare for a day of trekking.",
                        "Morning: Trek to the Jogini Waterfalls, a scenic trek that offers stunning views of the valley.",
                        "Afternoon: Enjoy a packed vegetarian lunch by the waterfalls.",
                        "Afternoon: Visit the Vashisht Hot Springs and take a relaxing dip in the natural hot water.",
                        "Evening: Return to Manali and unwind at a local café with some light snacks and tea."
                    ]
                },
                "day_3_7bdea8cb-42a0-4249-8ef6-774fae28e47e": {
                    "body": "Explore the cultural and historical aspects of Manali before heading back.",
                    "name": "Day 3",
                    "tips": [
                        "Keep your travel documents and valuables secure.",
                        "Plan your departure in advance to avoid any last-minute rush.",
                        "Buy some local souvenirs to remember your trip."
                    ],
                    "experiences_and_activities": [
                        "Morning: Have breakfast at the hostel and check out.",
                        "Morning: Visit the Manali Sanctuary, a great place for nature lovers and wildlife enthusiasts.",
                        "Afternoon: Explore the Old Manali area, known for its quaint cafes and shops.",
                        "Afternoon: Have a vegetarian lunch at one of the local cafes.",
                        "Evening: Visit the Manu Temple, dedicated to the sage Manu, and soak in the spiritual vibes.",
                        "Evening: Head back to the hostel to collect your luggage and prepare for departure."
                    ]
                }
            },
            "data_food_places": []
        },
        "updated_at": "2024-06-03T11:08:31.567218Z",
        "created_at": "2024-06-03T11:08:31.567162Z",
        "upvote_count": 0 } ]```

3. `http://localhost/karo_travel_plan/itinerary/8fa0568e-2258-4bf8-97b4-800d1015333c` - GET request to get data about each travel itiniary.


4. `http://localhost/karo_travel_plan/itinerary/8fa0568e-2258-4bf8-97b4-800d1015333c` - PATCH request to update day wise data about each travel itiniary.
    - Payload:
```
      {
            "day_1_79edaf7a-86fe-4283-9ef7-df2b71df1cc2": {
                "name": "Day 1",
                "tips": [],
                "experiences_and_activities": [],
                "body": "This is dummy"
      }
}   
```

5. `http://localhost/karo_travel_plan/itinerary/8fa0568e-2258-4bf8-97b4-800d1015333c` - DELETE request to update day wise data about each travel itiniary.
    - Response:
      - boolean value (True or False)
