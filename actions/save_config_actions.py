import telnetlib
import calendar
from datetime import datetime
import time
import os
import json
import ast
import requests
from dotenv import load_dotenv

load_dotenv()

sevone_url= os.getenv("SEVONE_URL")
auth_token= os.getenv("AUTH_TOKEN")
headers = {"Content-Type": "application/json", "X-AUTH-TOKEN": auth_token}
user = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
payload = {}
tftp_server = os.getenv("TFTP_SERVER")

def save_tmarc_configs():
    response = requests.request("GET", sevone_url, headers=headers, data=payload)
    devices = str(json.loads(response.text))
    device_dict = devices[devices.find("[")+1:devices.find("]")]
    devices_dict_str = "[" + device_dict + "]"
    device_list = ast.literal_eval(devices_dict_str)
    final_list = []

    for list in device_list:
        sub_list = {'hostname': list['name'], 'ip_address': list['ipAddress']}
        if "-250-" in list['name']:
            final_list.append(sub_list)
        if "-280-" in list['name']:
            final_list.append(sub_list)
        if "-340-" in list['name']:
            final_list.append(sub_list)
        if "-380-" in list['name']:
            final_list.append(sub_list)

    for device in final_list:
        now = datetime.now()
        file_name = device['hostname'] + "-" + now.strftime("%m_%d_%Y-%H_%M_%S")

        save_config_tmarc = f"copy running-config tftp://{tftp_server}/{file_name}.txt\n"
        save_config_250 = f"copy running-config upload-to {tftp_server} {file_name}.txt\n"
        copy_text = ""

        if "-250-" in device['hostname']:
            copy_text = save_config_250
        else:
            copy_text = save_config_tmarc

        copy_command = copy_text.encode()

        tn = telnetlib.Telnet(device['ip_address'])
        tn.read_until(b"Username:", timeout=2)
        tn.write(user.encode('ascii') + b"\n")

        tn.read_until(b"Password:")
        tn.write(password.encode('ascii') + b"\n")

        login_response = tn.read_until(b"Username", timeout=1)

        if b"Username" in login_response:
            continue

        tn.write(b"enable\n")

        time.sleep(.2)
        tn.write(copy_command)
        output = tn.expect([b"complete", b"failed"], timeout=10)
        print ("yay")


