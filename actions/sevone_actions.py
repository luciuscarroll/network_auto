import ast
import json
import os
import requests
from api_logins import sevone_api_login
from dotenv import load_dotenv

load_dotenv()

sevone_url = os.getenv("SEVONE_URL")
auth_token = sevone_api_login()
headers = {"Content-Type": "application/json", "X-AUTH-TOKEN": auth_token}
user = os.getenv("API_USER")
password = os.getenv("API_PASSWORD")
tftp_server = os.getenv("TFTP_SERVER")



def sevone_device_list():
    """This function pulls all the Devices from SEVONE."""
    token = sevone_api_login()
    headers["X-AUTH-TOKEN"] = token
    response = requests.request("GET", sevone_url, headers=headers)
    devices = str(json.loads(response.text))
    # Remove information outside of the [] so that the data shows up as an interger not a string.
    device_list = ast.literal_eval(f"[{devices[devices.find('[') + 1 : devices.find(']')]}]")
    return device_list


# TODO bult other functions to seprate device types.