from twilio.rest import Client
from flight_data import FlightData
import os

account_sid = os.environ.get("ACC_SID")
auth_token = os.environ.get("ACC_TOKEN")

client = Client(account_sid, auth_token)


class NotificationManager:

    def send_message(self, flight: FlightData):
        client.messages.create(
            body=f'Low price Alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}',
            from_='+17077766977',
            to='+54 11 6258 5363')
