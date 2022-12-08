import json
import os
import requests
from api_logins import sevone_api_login
from dotenv import load_dotenv
from schemas.devices import DeviceInfo, SevoneGroup
from pydantic import parse_obj_as
from typing import List

load_dotenv()

sevone_url = os.getenv("SEVONE_URL")
headers = {"Content-Type": "application/json", "X-AUTH-TOKEN": ""}
user = os.getenv("API_USER")
password = os.getenv("API_PASSWORD")
tftp_server = os.getenv("TFTP_SERVER")


def sevone_group_list():
    token = sevone_api_login()
    headers["X-AUTH-TOKEN"] = token
    response = requests.request("GET", f"{sevone_url}devicegroups?includeMembers=false&page=0&size=1000&includeCount=true", headers=headers)
    response_dict = json.loads(response.text)
    filtered_list = []
    for group in response_dict['content']:
        if group['parentId'] != 300:
            filtered_list.append(group)
    group_list = parse_obj_as(List[SevoneGroup], filtered_list)
    return group_list


def sevone_device_list(group_id):
    """This function pulls all the Devices from SEVONE."""
    token = sevone_api_login()
    headers["X-AUTH-TOKEN"] = token
    response = requests.request("GET", f"{sevone_url}devicegroups/{group_id}?includeMembers=true", headers=headers)
    response_dict = json.loads(response.text)
    device_list = []
    if response_dict['devices']:
       device_list = parse_obj_as(List[DeviceInfo], response_dict['devices'])
    return device_list
