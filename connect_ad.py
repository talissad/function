import requests
import uuid

from local_settings import *


def get_access_token():
    response = requests.post(url=AD_AUTHORITY, data=LOGIN_DATA)
    access_token = response.json()['access_token']
    return access_token

def call_endpoint(access_token, path):
    endpoint = f'https://graph.microsoft.com/v1.0/{path}'
    http_headers = {'Authorization': access_token,
                    'User-Agent': 'adal-python-sample',
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'client-request-id': str(uuid.uuid4())}
    response = requests.get(endpoint, headers=http_headers)
    if response.status_code == 200:
        return response.json()
    raise Exception(response.content)

def execute(path):
    access_token = get_access_token()
    response = call_endpoint(access_token, path)
    for item in response['value']:
        if "displayName" in item and "id" in item:
            print(f"{item['id']} - {item['displayName']}")
    return response
