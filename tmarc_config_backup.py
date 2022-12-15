import json
import os
import requests
import telnetlib
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

sevone_url = os.getenv("SEVONE_URL")
headers = {"Content-Type": "application/json", "X-AUTH-TOKEN": ""}
user = os.getenv("API_USER")
password = os.getenv("API_PASSWORD")
tftp_server = os.getenv("TFTP_SERVER")

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


def get_all_tmarcs():
    """gets all devices from Sevone, returns only the tmarc devices."""
    token = sevone_api_login()
    headers["X-AUTH-TOKEN"] = token
    response = requests.request("GET", f"{sevone_url}devicegroups/298?includeMembers=true", headers=headers)
    response_dict = json.loads(response.text)
    return response_dict["devices"]


def save_tmarc_configs():
    """Gets Devices from SEVONE. Sorts the Tmarcs into a list. Save and copies configs"""

    tmarc_list = get_all_tmarcs()


    for device in tmarc_list:
        now = datetime.now()
        file_name = device["name"] + "-" + now.strftime("%m_%d_%Y-%H_%M")
        save_config_tmarc = (
            f"copy running-config tftp://{tftp_server}/{file_name}.txt\n"
        )
        save_config_250 = (
            f"copy running-config upload-to {tftp_server} {file_name}.txt\n"
        )
        copy_config_command = ""

        if "-250-" in device["name"]:
            copy_config_command = save_config_250
        else:
            copy_config_command = save_config_tmarc

        copy_command = copy_config_command.encode()

        try:
            tn = telnetlib.Telnet(device["ipAddress"])
            tn.read_until(b"Username:", timeout=2)
            tn.write(user.encode("ascii") + b"\n")

            tn.read_until(b"Password:")
            tn.write(password.encode("ascii") + b"\n")

            login_response = tn.read_until(b"Username", timeout=1)
            if b"Username" in login_response:
                continue

            tn.write(b"enable\n")
            # Sleep here so the tmarc has time to output data.
            time.sleep(0.2)

            tn.write(b"write\n")
            # Sleep here for 2 sec so tmarc has time to write config to memory.
            time.sleep(2)

            tn.write(copy_command)
            # Sleep here so the tmarc has time to push files to the tftp server.
            time.sleep(4)
            tn.write(b"exit\n")
            
        except TimeoutError as e:
            print(device["name"])
            print(str(e))
            print("***************************")
            continue
    print("Done.")

if __name__ == "__main__":
    save_tmarc_configs()