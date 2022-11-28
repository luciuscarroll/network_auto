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


def save_tmarc_configs():
    """Gets Devices from SEVONE. Sorts the Tmarcs into a list. Save and copies configs"""

    device_list = sevone_actions.sevone_device_list()
    tmarc_list = []
    count = 0
    # TODO remove this count eventually.

    for list in device_list:
        formatted_device = {"hostname": list["name"], "ip_address": list["ipAddress"]}
        # Don't use this formatting again. It is just easier to leave it here.
        if "-250-" in list["name"]:
            tmarc_list.append(formatted_device)
        if "-280-" in list["name"]:
            tmarc_list.append(formatted_device)
        if "-340-" in list["name"]:
            tmarc_list.append(formatted_device)
        if "-380-" in list["name"]:
            tmarc_list.append(formatted_device)

    for device in tmarc_list:
        now = datetime.now()
        file_name = device["hostname"] + "-" + now.strftime("%m_%d_%Y-%H_%M_%S")
        save_config_tmarc = (
            f"copy running-config tftp://{tftp_server}/{file_name}.txt\n"
        )
        save_config_250 = (
            f"copy running-config upload-to {tftp_server} {file_name}.txt\n"
        )
        copy_config_command = ""

        if "-250-" in device["hostname"]:
            copy_config_command = save_config_250
        else:
            copy_config_command = save_config_tmarc
        # https://docs.python.org/3/library/telnetlib.html
        copy_command = copy_config_command.encode()

        tn = telnetlib.Telnet(device["ip_address"])
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
        count += 1
        print(count)
        # Print the Count to the console to make me feel like things are working.

        time.sleep(1)
        # Waits for 1 second between Tmarcs to help my work computer not lose its brains.


# TODO look into shipping files to ftp server once they are collected locally.
# https://docs.python.org/3/library/ftplib.html
