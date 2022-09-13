from netmiko import ConnectHandler
from dotenv import load_dotenv
import os

load_dotenv()

device_type= os.getenv('DEVICE_TYPE')
host= os.getenv('HOST')
username= os.getenv('USERNAME')
password= os.getenv('PASSWORD')


ssh_rsvt = ConnectHandler(
    device_type=device_type,
    host=host,
    username=username,
    password=password
)


def clearBinding(remote_id):
    # Get mac address by remote ID
    response_rsvt = ssh_rsvt.send_command(f"show dhcp ipv4 proxy binding remote-id {remote_id}")
    binding_details = {
        "mac_address": None,
        "vrf": None,
        "ip_address": None,
        "server_vrf": None,
        "giaddr_from_client": None,
        "giaddr_to_server": None,
        "server_ip_address_to_client": None,
        "server_ip_address": None,
        "received_circuit_id": None,
        "insert_circuit_id": None,
        "received_remote_id": None,
        "inserted_remote_id": None,
        "recieved_VSISO": None,
        "inserted_VSISO": None,
        "Auth_on_recieved_relay": None,
        "param_request_option": None,
        "saved_options": None,
        "profile": None,
        "state": None,
        "lease": None,
        "lease_remaining": None,
        "client_id": None,
        "access_interface": None,
        "access_vrf": None,
        "subsriber_label": None,
        "srg_state": None,
        "event_history": None,
        "session_start": None,
        "packet_discover": None,
        "dpm_success": None,
        "packet_offer": None,
        "packet_request": None,
        "packet_ack": None,
        "lease_dpm_success": None,
        'route_success': None
    }

    lines = response_rsvt.split("\n")
    for line in lines:
        if ":" in line:
            split_line = line.split(":")
            if split_line[0] == "MAC Address":
                split_line[1] = split_line[1].strip()
                binding_details["mac_address"] = split_line[1]
            elif split_line[0] == "VRF":
                split_line[1] = split_line[1].strip()
                binding_details["vrf"] = split_line[1]
            elif split_line[0] == "Server VRF":
                split_line[1] = split_line[1].strip()
                binding_details["server_vrf"] = split_line[1] 
            elif split_line[0] == "IP Address":
                split_line[1] = split_line[1].strip()
                binding_details["ip_address"] = split_line[1]   
            elif split_line[0] == "Giaddr from client":
                split_line[1] = split_line[1].strip()
                binding_details["giaddr_from_client"] = split_line[1]
            elif split_line[0] == "Giaddr to server":
                split_line[1] = split_line[1].strip()
                binding_details["giaddr_to_server"] = split_line[1]
            elif split_line[0] == "Server IP Address to client":
                split_line[1] = split_line[1].strip()
                binding_details["server_ip_address_to_client"] = split_line[1] 
            elif split_line[0] == "Server IP Address":
                split_line[1] = split_line[1].strip()
                binding_details["server_ip_address"] = split_line[1]                         
            elif split_line[0] == "ReceivedCircuit ID":
                split_line[1] = split_line[1].strip()
                binding_details["received_circuit_id"] = split_line[1]
            elif split_line[0] == "InsertedCircuit ID":
                split_line[1] = split_line[1].strip()
                binding_details["inserted_circuit_id"] = split_line[1]
            elif split_line[0] == "ReceivedRemote ID":
                split_line[1] = split_line[1].strip()
                binding_details["received_remote_id"] = split_line[1] 
            elif split_line[0] == "InsertedRemote ID":
                split_line[1] = split_line[1].strip()
                binding_details["inserted_remote_id"] = split_line[1] 
            elif split_line[0] == "ReceivedVSISO":
                split_line[1] = split_line[1].strip()
                binding_details["recieved_VSISO"] = split_line[1]    
            elif split_line[0] == "InsertedVSISO":
                split_line[1] = split_line[1].strip()
                binding_details["inserted_VSISO"] = split_line[1]   
            elif split_line[0] == "Auth. on received relay info":
                split_line[1] = split_line[1].strip()
                binding_details["Auth_on_recieved_relay"] = split_line[1]      
            elif split_line[0] == "ParamRequestOption":
                split_line[1] = split_line[1].strip()
                binding_details["param_request_option"] = split_line[1]  
            elif split_line[0] == "SavedOptions":
                split_line[1] = split_line[1].strip()
                binding_details["saved_options"] = split_line[1]  
            elif split_line[0] == "Profile":
                split_line[1] = split_line[1].strip()
                binding_details["profile"] = split_line[1] 
            elif split_line[0] == "State":
                split_line[1] = split_line[1].strip()
                binding_details["state"] = split_line[1]  
            elif split_line[0] == "Lease":
                split_line[1] = split_line[1].strip()
                binding_details["lease"] = split_line[1]  
            elif split_line[0] == "Client ID":
                split_line[1] = split_line[1].strip()
                binding_details["client_id"] = split_line[1]  
            elif split_line[0] == "Access Interface":
                split_line[1] = split_line[1].strip()
                binding_details["access_interface"] = split_line[1] 
            elif split_line[0] == "Access VRF":
                split_line[1] = split_line[1].strip()
                binding_details["access_vrf"] = split_line[1] 
            elif split_line[0] == "Subscriber Label":
                split_line[1] = split_line[1].strip()
                binding_details["subscriber_label"] = split_line[1]   
            elif split_line[0] == "Srg State":
                split_line[1] = split_line[1].strip()
                binding_details["srg_state"] = split_line[1]   
            elif split_line[0] == "Event History":
                split_line[1] = split_line[1].strip()
                binding_details["event_history"] = split_line[1]  
            elif split_line[0] == "Session Start":
                split_line[1] = split_line[1].strip()
                binding_details["sesstion_start"] = split_line[1]  
            elif split_line[0] == "PACKET_DISCOVER":
                split_line[1] = split_line[1].strip()
                binding_details["packet_discover"] = split_line[1] 
            elif split_line[0] == "DPM_SUCCESS":
                split_line[1] = split_line[1].strip()
                binding_details["dpm_success"] = split_line[1]    
            elif split_line[0] == "PACKET_OFFER":
                split_line[1] = split_line[1].strip()
                binding_details["packet_offer"] = split_line[1] 
            elif split_line[0] == "PACKET_REQUEST":
                split_line[1] = split_line[1].strip()
                binding_details["packet_request"] = split_line[1]  
            elif split_line[0] == "PACKET_ACK":
                split_line[1] = split_line[1].strip()
                binding_details["packet_ack"] = split_line[1]  
            elif split_line[0] == "LEASE_DPM_SUCCESS":
                split_line[1] = split_line[1].strip()
                binding_details["lease_dpm_success"] = split_line[1] 
            elif split_line[0] == "ROUTE_SUCCESS":
                split_line[1] = split_line[1].strip()
                binding_details["route_success"] = split_line[1]
            elif split_line[0] == "Lease remaining":
                split_line[1] = split_line[1].strip()
                binding_details["lease_remaining"] = split_line[1]   
            else:
                print("not found")
               
            #if "MAC Address" in line:
                #mac_address = line.split()[2]
                # Clears mac address binded to remote id
                #ssh_rsvt.send_command(f"clear dhcp ipv4 proxy binding mac-address {mac_address}")
    if binding_details["mac_address"]:
        response=ssh_rsvt.send_command(f"clear dhcp ipv4 proxy binding mac-address {binding_details['mac_address']}")
        return({"status": 200, "message": f"Binding cleared for RSVT {remote_id}"})    
    else:
        return({"status": 404, "message": f"Binding not found"})

def runClearBinding(remote_id):
    response = clearBinding(remote_id)
    # Disconnects from Cisco Router
    ssh_rsvt.disconnect()
    return response

    
