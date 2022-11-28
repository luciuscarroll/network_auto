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
payload = {}
tftp_server = os.getenv("TFTP_SERVER")

def sevone_device_list():
    # This function pulls all the Devices from SEVONE.
    # Logs into SEVONE to pull a list of all devices.
    token = sevone_api_login()
        # Create SEVONE API token.
        # This is done from the root directory in file api_logins.py.
    headers["X-AUTH-TOKEN"] = token
        # Set headers postion X-AUTH-TOKEN equal to the SEVONE API token.
    response = requests.request("GET", sevone_url, headers=headers, data=payload)
        # Calls SEVONE API for all a list of all devices.
        # sevone_url is pulled from the .env file.
        # headers postion Content-Type is hardset to application/json
        # headers postion X-AUTH-TOKEN is set to the sevone API token generated above.
        # TODO I am unsure what the data=payload line is doing. Need to look into it.
    devices = str(json.loads(response.text))
        # Here we have the full Device list from SEVONE. This is in JSON format.
    device_list = ast.literal_eval(f"[{devices[devices.find('[') + 1 : devices.find(']')]}]")
        # Finding the [] in the output and discarding the information outside of them.
        # https://docs.python.org/3/library/ast.html
        # This creates the Device list dictionary. This is dictionary can be used to sort out devices.
    return device_list