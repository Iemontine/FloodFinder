import os
from dotenv import load_dotenv
import http.client
import json

load_dotenv()
serper_api_key = os.getenv('SERPER_API_KEY')

def research_coordinates(location):
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
   		"q": f"coordinates of {location}"
    })
    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = (json.loads(res.read().decode("utf-8")))
    return data['organic'][0]['snippet']