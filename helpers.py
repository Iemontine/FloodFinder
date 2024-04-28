import os
from dotenv import load_dotenv
import http.client
import json

load_dotenv()
browserless_api_key = os.getenv('BROWSERLESS_API_KEY')
serper_api_key = os.getenv('SERPER_API_KEY')

def search(query):
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
    "q": query
    })
    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = (json.loads(res.read().decode("utf-8")))
    print(data['organic'][0]['snippet'])
    
search("What are the coordinates of Los Angles, CA?")


