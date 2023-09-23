from datetime import datetime, timedelta
from pprint import pprint
from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager


sheet_data = DataManager.get_sheet_data(None)

sheet_data_with_code = [(lambda r: {**r, 'iataCode': FlightSearch.get_code(None, r['city'])})(row) for row in sheet_data if row['iataCode'] == '']

DataManager.update_sheet_data(None, sheet_data_with_code)

tomorrow = datetime.now() + timedelta(days=1)
six_months_from_today = datetime.now() + timedelta(days=(6*30))

pprint(sheet_data_with_code)

if len(sheet_data_with_code) != 0:
    data = sheet_data_with_code
else:
    data = sheet_data

for row in data:
    flight = FlightSearch.check_flights(None, 'LON', row['iataCode'], tomorrow, six_months_from_today)

    data_row = [r for r in data if r['iataCode'] == row['iataCode'] and r['lowestPrice'] > flight.price]

    if len(data_row) > 0:
        NotificationManager.send_message(None, flight)






