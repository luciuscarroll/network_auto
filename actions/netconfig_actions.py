import imp
from ncclient import manager
from dotenv import load_dotenv
import os

load_dotenv()

device_type= os.getenv('DEVICE_TYPE')
host= os.getenv('HOST')
username= os.getenv('USERNAME')
password= os.getenv('PASSWORD')


mgr_lab = manager.connect()