import os

from dotenv import load_dotenv
from netmiko import ConnectHandler

load_dotenv()

username = os.getenv("API_USER")
password = os.getenv("API_PASSWORD")


def get_connection(device_type, host):
    ssh_session = ConnectHandler(
        device_type=device_type, host=host, username=username, password=password
    )
    return ssh_session
