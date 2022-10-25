from schemas.Configs import PhysicalInterface, DhcpBinding

def clearBinding(ssh_connection,remote_id)->DhcpBinding:
    # Get mac address by remote ID
    
    response_rsvt = ssh_connection.send_command(f"show dhcp ipv4 proxy binding remote-id {remote_id}")
    binding_details = DhcpBinding()

    lines = response_rsvt.split("\n")
    for line in lines:
        if ":" in line:
            split_line = line.split(":")
            if split_line[0] == "MAC Address":
                split_line[1] = split_line[1].strip()
                binding_details.mac_address = split_line[1]
            #if "MAC Address" in line:
                #mac_address = line.split()[2]
                #Clears mac address bound to remote id
                #ssh_rsvt.send_command(f"clear dhcp ipv4 proxy binding mac-address {mac_address}")
    if binding_details.mac_address:
        ssh_connection.send_command(f"clear dhcp ipv4 proxy binding mac-address {binding_details.mac_address}")
        return True    
    else:
        return False


def transciever_phy(ssh_connection,transciever)->PhysicalInterface:
    response_rsvt = ssh_connection.send_command(f"show controllers {transciever} phy")
    transciever_details = PhysicalInterface()

    lines = response_rsvt.split("\n")
    for line in lines:
        if ":" in line:
            line = line.replace("\t","")
            split_line = line.split(":")
            if split_line[0] == "Xcvr Type":
                split_line[1] = split_line[1].strip()
                transciever_details.transciever_type = split_line[1]
            elif split_line[0] == "Xcvr Code":
                split_line[1] = split_line[1].strip()
                transciever_details.transciever_part_number = split_line[1]
            elif split_line[0] == "Laser wavelength":
                split_line[1] = split_line[1].strip()
                details = split_line[1].split(" (")
                transciever_details.laser_wavelength = details[0]
            elif split_line[0] == "Tx Power":
                split_line[1] = split_line[1].strip()
                transciever_details.transmit_power = split_line[1]
            elif split_line[0] == "Rx Power":
                split_line[1] = split_line[1].strip()
                transciever_details.recieve_power = split_line[1]
            elif split_line[0] == "Vendor Name":
                split_line[1] = split_line[1].strip()
                transciever_details.vendor_name = split_line[1]
            elif split_line[0] == "PHY data for interface":
                split_line[1] = split_line[1].strip()
                transciever_details.interface = split_line[1]
    if transciever_details != None:
        return transciever_details
    else:
        return None
