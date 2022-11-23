from netmiko import ConnectHandler
from dotenv import load_dotenv
import os

load_dotenv()

device_type= os.getenv('DEVICE_TYPE')
host= os.getenv('HOST')
username= os.getenv('USERNAME')
password= os.getenv('PASSWORD')

def get_connection():
    ssh_rsvt = ConnectHandler(
        device_type=device_type,
        host=host,
        username=username,
        password=password
    )
    return ssh_rsvt

