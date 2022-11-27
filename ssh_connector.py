import os

from dotenv import load_dotenv
from netmiko import ConnectHandler

load_dotenv()

device_type = os.getenv("DEVICE_TYPE")
host = os.getenv("HOST")
username = os.getenv("API_USER")
password = os.getenv("PASSWORD")


def get_connection():
    ssh_rsvt = ConnectHandler(
        device_type=device_type, host=host, username=username, password=password
    )
    return ssh_rsvt
