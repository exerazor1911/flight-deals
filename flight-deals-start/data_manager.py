import requests
import os

SHEET_GET = os.environ.get('SHEET_GET')
SHEET_PUT = os.environ.get('SHEET_PUT')


class DataManager:

    def get_sheet_data(self):
        response = requests.get(SHEET_GET)
        response.raise_for_status()
        return response.json()['prices']

    def update_sheet_data(self, json):
        for row in json:
            url = SHEET_PUT.replace('[Object ID]', str(row['id']))
            body = {
                'price': {
                    'iataCode': row['iataCode'],
                }
            }
            response = requests.put(url=url, json=body)
