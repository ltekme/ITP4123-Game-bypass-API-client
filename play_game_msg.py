import requests
from urllib.parse import quote_plus
from dotenv import dotenv_values
from _modules import HEADERS

API_URL = 'https://kp4du9furk.execute-api.us-east-1.amazonaws.com/api'

for i in range(5):
    api_response = requests.get(
        f'{API_URL}/game?mode=game&api_key={quote_plus(dotenv_values(".config").get("API_KEY"))+"&"}', headers=HEADERS)
    if api_response.status_code != 200:
        print("None")
        continue
    print(api_response.content.decode('utf-8'))
