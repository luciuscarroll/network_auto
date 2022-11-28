import os
import telnetlib
import time
from datetime import datetime
from actions import sevone_actions
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("API_USER")
password = os.getenv("API_PASSWORD")
tftp_server = os.getenv("TFTP_SERVER")

# TODO look into shipping files to ftp server once they are collected locally.
# https://docs.python.org/3/library/ftplib.html

def save_tmarc_configs():
    """Gets Devices from SEVONE. Sorts the Tmarcs into a list. Save and copies configs"""

    device_list = sevone_actions.sevone_device_list()
    tmarc_list = []

    for device in device_list:
        if "-250-" in device["name"]:
            tmarc_list.append(device)
        if "-280-" in device["name"]:
            tmarc_list.append(device)
        if "-340-" in device["name"]:
            tmarc_list.append(device)
        if "-380-" in device["name"]:
            tmarc_list.append(device)

    for device in tmarc_list:
        now = datetime.now()
        file_name = device["name"] + "-" + now.strftime("%m_%d_%Y-%H_%M_%S")
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
        # https://docs.python.org/3/library/telnetlib.html
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
            # sleep here for 2 sec so tmarc has time to write config to memory.
            time.sleep(2)

            tn.write(copy_command)
            time.sleep(2)
            # check how long it takes to send file and change sleep timer.
            tn.write(b"exit\n")

            time.sleep(1)
            # Waits for 1 second between Tmarcs to help my work computer not lose its brains.
        except Exception as e:
            print(device["name"])
            print(str(e))
            print("***************************")
            continue
    print("Done.")
# TimeoutError