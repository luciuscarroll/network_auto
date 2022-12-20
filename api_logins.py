import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

def sevone_api_login():
    url = os.getenv("SEVONE_URL")

    payload = json.dumps({
    "name": os.getenv("SEVONE_API_USER"),
    "password": os.getenv("SEVONE_API_PASS")
    })
    headers = {
    'Content-Type': 'application/json',
    }

    response = requests.request("POST", f"{url}authentication/signin", headers=headers, data=payload)

    to_dict = json.loads(response.text)
    token = to_dict["token"]

    return token