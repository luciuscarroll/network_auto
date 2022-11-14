from schemas.Configs import PhysicalInterface, DhcpBinding, OSPF

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


def transciever_phy_cisco_xr(ssh_connection,transciever)->PhysicalInterface:
    # Get Cisco XR Physical port information
    response_controller = ssh_connection.send_command(f"show controllers {transciever} all")
    transciever_details = PhysicalInterface()

    lines = response_controller.split("\n")
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
            elif split_line[0] == "    Administrative state":
                split_line[0] = split_line[1].strip()
                transciever_details.admin_state = split_line[1]
    if transciever_details != None:
        return transciever_details
    else:
        return None

def transciever_phy_cisco_xe(ssh_connection,transciever)->PhysicalInterface:
    # Get Cisco XE Physical port information
    transciever_split = transciever.split("/")
    response_status = ssh_connection.send_command(f"show hw-module subslot 0/{transciever_split[1]} transceiver {transciever_split[2]} status")
    response_idprom = ssh_connection.send_command(f"show hw-module subslot 0/{transciever_split[1]} transceiver {transciever_split[2]} idprom detail")
    module_details = PhysicalInterface()
    status = response_status.split("\n")
    status.pop(0)
    idprom = response_idprom.split('\n')
    for line in idprom:
        split_line = line.split(" ")
        split_line[0] = split_line[0].strip()
        if split_line[0] == "IDPROM":
            module_details.interface = split_line[3]
    idprom.pop(0)
    for line in status:
        split_line = line.split("= ")
        split_line[0] = split_line[0].strip()
        if split_line[0] == "Transceiver Tx power":
            module_details.transmit_power = split_line[1]
        elif split_line[0] == "Transceiver Rx optical power":
            module_details.recieve_power = split_line[1]
    for line in idprom:
        split_line = line.split("= ")
        split_line[0] = split_line[0].strip()   
        if split_line[0] == "Transceiver Type:":
            module_details.transciever_type = split_line[1]
        elif split_line[0] == "Cisco part number":
            module_details.transciever_part_number = split_line[1]
        elif split_line[0] == "Vendor Name":
            module_details.vendor_name = split_line[1]
        elif split_line[0] == "DWDM wavelength fraction":
            module_details.laser_wavelength = split_line[1]
        elif split_line[0]  == "Device State":
            module_details.admin_state = split_line[1]
    if module_details != None:
        return module_details
    else:
        return None

def ospf(ssh_connection)->OSPF:
    # Get Cisco XR OSPF information.
    response_neighbor_detail = ssh_connection.send_command("show ospf neighbor detail")
    ospf_neighbor_details = OSPF()
    neighbor_details = response_neighbor_detail.split("\n")
    neighbor_details.pop(0,1,2)
    for line in neighbor_details:
        split_line = line.split(" ")
        split_line[0] = split_line[0].strip()
        if split_line[0] == "Neighbor":
            ospf_neighbor_details.neighbor_id = split_line[1]
    if neighbor_details != None:
        return neighbor_details
    else:
        return None
