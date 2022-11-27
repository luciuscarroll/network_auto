import ast
import json
import os
import telnetlib
import time
from datetime import datetime
import requests
from dotenv import load_dotenv
from api_logins import sevone_api_login

load_dotenv()

sevone_url = os.getenv("SEVONE_URL")
auth_token = sevone_api_login()
headers = {"Content-Type": "application/json", "X-AUTH-TOKEN": auth_token}
user = os.getenv("API_USER")
password = os.getenv("API_PASSWORD")
payload = {}
tftp_server = os.getenv("TFTP_SERVER")


def save_tmarc_configs():
    # This function pulls all the Devices from SEVONE. Then checks the device portion of the hostname. Sorts the Tmarc deives types into a list.
    # It then splits the Tmarcs into groups to run the correct copy config command.
    # After that it sets up the TELNET session to the Tmarc and sends a write config and copy config command.
    # TODO move from toekn to device_list to another file. so it can be easily used by other functions.
    # Logs into SEVONE to pull a list of all devices. Then sorts out the Tmarcs into a seperate list.
    token = sevone_api_login()
    # Create SEVONE API token.
    # This is done from the root directory from file api_logins.py.
    headers["X-AUTH-TOKEN"] = token
    # Set headers postion X-AUTH-TOKEN equal to the SEVONE API token.
    response = requests.request("GET", sevone_url, headers=headers, data=payload)
    # Calls SEVONE API for all a list of all devices.
    # sevone_url is pulled from the .env file.
    # headers postion Content-Type is hardset to application/json
    # headers postion X-AUTH-TOKEN is set to the sevone API token generated above.
    # TODO I am unsure what the data=payload line is doing. Need to look into it.
    devices = str(json.loads(response.text))
    # Here we have the full Device list from SEVONE. We now break it down into a usable format.
    # TODO Need to run through it in debugger and see if this can be simplified.
    device_dict = devices[devices.find("[") + 1 : devices.find("]")]
    # TODO Need to understand this better.
    # TODO Need to run through it in debugger and see if this can be simplified.
    devices_dict_str = "[" + device_dict + "]"
    # TODO Need to understand this better.
    # TODO Need to run through it in debugger and see if this can be simplified.
    device_list = ast.literal_eval(devices_dict_str)
    # This creates the Device list dictionary. This is the dictionary we will use to sort out devices.
    # TODO Need to understand this better.
    # TODO Need to run through it in debugger and see if this can be simplified.
    tmarc_list = []
    # This is the tmarc list generated from the for list in device_list loop below.
    count = 0
    # This is used to show that the program is progressing in the terminal.

    for list in device_list:
        # Here we take the device_list from SEVONE and pull out just the Tmarcs.
        temp_list = {"hostname": list["name"], "ip_address": list["ipAddress"]}
        # Create a temporary list, temp_list, if the hostname/name has a tmarc device type, I.E. 250,280,340,280, append it to tmarc_list.
        # TODO need to understand the temp_list more to explain this better.
        if "-250-" in list["name"]:
            tmarc_list.append(temp_list)
        if "-280-" in list["name"]:
            tmarc_list.append(temp_list)
        if "-340-" in list["name"]:
            tmarc_list.append(temp_list)
        if "-380-" in list["name"]:
            tmarc_list.append(temp_list)

    for device in tmarc_list:
        # Here we take the tmarc_list generated form the device_list.
        # With this list we decide if the Tmarc falls into one of two groups. Is it a 250 or not a 250?
        # Then we log into the Tmarc using TELNET and send the enable, write config, and copy config to tftp server commands.
        # the loop will then move to the next Tmarc in the list and run through all the steps again.

        now = datetime.now()
        # Set now equal to the current system time using the python datetime library.
        # TODO I never checked the time stamp for accuracy. when reading through the datetime library documentation found that the timezone may need set.
        # https://docs.python.org/3/library/datetime.html
        file_name = device["hostname"] + "-" + now.strftime("%m_%d_%Y-%H_%M_%S")
        # Set file_name equal to the hostname of the device followed by a dash then the mounth day year hour minute second the file name created.
        # almt-ac-380-example-1_23_2022-4_32_47

        save_config_tmarc = (
            f"copy running-config tftp://{tftp_server}/{file_name}.txt\n"
        )
        # Above it the copy command for Tmarc models 280, 340 and 380. This includes the standard parts of the config, the tftp server and the filename generated above followed by .txt to make it a text file.
        save_config_250 = (
            f"copy running-config upload-to {tftp_server} {file_name}.txt\n"
        )
        # Above it the copy command for Tmarc model 250. This includes the standard parts of the config, the tftp server and the filename generated above followed by .txt to make it a text file.
        copy_config_command = ""
        # This is an empty string that will be filed with either the save_config_tmarc or save_config_250 later on.

        if "-250-" in device["hostname"]:
            copy_config_command = save_config_250
        else:
            copy_config_command = save_config_tmarc
        # This is were we decide if the Tmarc is or is not a 250 and then copies the correct command.

        # Below is a link for handy information for the python telnetlib used below.
        # https://docs.python.org/3/library/telnetlib.html
        # .encode takes what ever command you are sending and converts it into ASCII format that is compatible with TELNET.
        copy_command = copy_config_command.encode()
        # This copies the text of the command.

        tn = telnetlib.Telnet(device["ip_address"])
        # From python telnetlib use telnet to connect to the device ip address in the device in tmarc_list.
        tn.read_until(b"Username:", timeout=2)
        # Once connected wait for Username to shows up from the output of the Tmarc.
        tn.write(user.encode("ascii") + b"\n")
        # Now we send in the user which is set equal to API_USER from the .env file imported above.

        tn.read_until(b"Password:")
        # Once the user is sent we wait until Password shows up from the output of the Tmarc.
        tn.write(password.encode("ascii") + b"\n")
        # Now we send in the password which is set equal to PASSWORD from the .env file imported above.

        login_response = tn.read_until(b"Username", timeout=1)
        # This tracks the login until Username shows up

        if b"Username" in login_response:
            # This requires that Username shows up in the login response before sending in the above commands. if it isn't it will not continue.
            continue

        tn.write(b"enable\n")
        # Once logged in send in the enable command to to chnage the switch to privledge mode to accept copy commands.

        time.sleep(0.2)
        tn.write(b"write\n")
        # Now we wait a fraction of a second then send in the write command.

        time.sleep(2)
        tn.write(copy_command)
        # We now wait two seconds to allow the write command to finish then send in the copy command to the Tmarc that send the config to a TFTP server.

        output = tn.expect([b"complete", b"failed"], timeout=10)
        # not sure this is doing anything

        count += 1
        # Adds 1 to the count after each Tmarc is completed.

        print(count)
        # Print the Count to the console to make me feel like things are working.

        time.sleep(1)
        # Waits for 1 second between Tmarcs to help my work computer not lose its brains.
