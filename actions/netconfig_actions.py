from ncclient import manager
from dotenv import load_dotenv
import os

load_dotenv()

device_type= os.getenv('DEVICE_TYPE')
host= os.getenv('HOST')
username= os.getenv('USERNAME')
password= os.getenv('PASSWORD')
filter_controller_optics = """
<filter>
    <controller xmls="urn:ietf:params:xml:ns:yang:ietf-controller-optics">
        <optics>
        </optics>
    </controller>
</filter>
"""


# mgr_lab = manager.connect(
#     host = host,
#     username = username,
#     password = password,
#     hostkey_verify = False
# )

def getconfig():
    mgr_lab = manager.connect(
        host = host,
        username = username,
        password = password,
        hostkey_verify = False
    )
    for capabilitiy in mgr_lab.server_capabilities:
        print(capabilitiy)
