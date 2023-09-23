import requests
from flight_data import FlightData
import os

TEQUILA_URL = 'https://api.tequila.kiwi.com'
KEY = os.environ.get("TEKILA_KEY")


class FlightSearch:

    def fill_iata_code(self, cities, json):
        for row in json:
            if row['city'] in cities:
                row['iataCode'] = 'TESTING'

    def get_code(self, city):
        header = {
            'apiKey': KEY
        }
        params = {
            'term': city,
            'location_types': 'city'
        }

        response = requests.get(url=f'{TEQUILA_URL}/locations/query', headers=header, params=params)
        response.raise_for_status()
        return response.json()['locations'][0]['code']

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {
            'apiKey': KEY
        }
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }

        response = requests.get(
            url=f"{TEQUILA_URL}/v2/search",
            headers=headers,
            params=query,
        )

        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        print(f"{flight_data.destination_city}: £{flight_data.price}")
        return flight_data
