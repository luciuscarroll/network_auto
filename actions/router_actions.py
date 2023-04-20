from schemas.Configs import OSPF, OSPF_NeighborDetails, PhysicalInterface
from netmiko import ConnectHandler
from schemas.enums import Router_Enum

def split_line(line):
    line = line.strip()
    split_line = line.split(" ")
    return split_line

def ospf_neighbor_cisco_xr(ssh_connection)->list[OSPF]:
    # Get Cisco XR OSPF information.
    response_neighbor_detail = ssh_connection.send_command("show ospf neighbor detail")
    if response_neighbor_detail == None:
        return None
    raw_ospf = response_neighbor_detail.split("\n\n")
    raw_ospf = raw_ospf[3:]
    ospf = OSPF(
        ospf_raw_details= response_neighbor_detail
        )
    for raw_neighbor in raw_ospf:
        #TODO add part to deal with differnt ospf processes ie 1 and 30432
        lines = raw_neighbor.split("\n")
        if 'Total neighbor count:' in raw_neighbor:
            # ospf.total_neighbor_count = split_line(raw_neighbor)[3]
            continue
        ospf_neighbor = OSPF_NeighborDetails()
        for line in lines:
            line_list = split_line(line)
            if "Neighbor" and "interface address" in line:
                ospf_neighbor.neighbor = line_list[1].replace(",","")
                ospf_neighbor.interface_address = line_list[4]
            if "In the area" in line:
                ospf_neighbor.area = line_list[3]
                ospf_neighbor.interface = line_list[6]
            if "Neighbor priority" in line:
                ospf_neighbor.neighbor_priority = line_list[3].replace(",","")
                ospf_neighbor.state = line_list[6].replace(",","")
                ospf_neighbor.state_changes = line_list[7]
            if "DR is" in line:
                ospf_neighbor.designated_router = line_list[2]
                ospf_neighbor.backup_designated_router = line_list[5]
            if "    Options is " in line:
                ospf_neighbor.options = line_list[2]
            if "LLS Options" in line:
                ospf_neighbor.lls_options = f"{line_list[3]} {line_list[4]}"
            if "Dead timer due" in line:
                ospf_neighbor.dead_timer = line_list[4]
            if "Neighbor is up" in line:
                ospf_neighbor.neighbor_uptime = line_list[4]
            if "Number of" in line:
                ospf_neighbor.dbd_retrans_last_exchange = line_list[7]
            if "Index" in line:
                ospf_neighbor.index = line_list[1].replace(",","")
                ospf_neighbor.retransmission_queue_length = line_list[5].replace(",","")
                ospf_neighbor.retansmission_number = line_list[9]
            if "First" in line:
                ospf_neighbor.first = line_list[1]
                ospf_neighbor.next = line_list[3]
            if "scan length" in line:
                ospf_neighbor.last_retransmission_scan_length = line_list[5].replace(",","")
                ospf_neighbor.last_retransmission_scan_length_max = line_list[8]
            if "scan time" in line:
                ospf_neighbor.last_retransmission_scan_time = f"{line_list[5]} msec"
                ospf_neighbor.last_retransmission_scan_time_max = f"{line_list[9]} msec"
            if "LS Ack" in line:
                ospf_neighbor.ls_ack_list = line[17:]
        ospf.ospf_details.append(ospf_neighbor)
    ospf.total_neighbor_count = len(ospf.ospf_details)
    return ospf

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
    response_status = ssh_connection.send_command(f"show hw-module subslot 0/{transciever_split[1]} transciever {transciever_split[2]} status")
    response_idprom = ssh_connection.send_command(f"show hw-module subslot 0/{transciever_split[1]} transciever {transciever_split[2]} idprom detail")
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

def get_physical_interface(connection: ConnectHandler, transciever: str, device_type: Router_Enum) -> PhysicalInterface:
    interface = None
    # TODO make call to get port speed for transciever
    transciever = f"te{transciever}"
    if device_type == Router_Enum.CISCO_XE:
        interface = transciever_phy_cisco_xe(ssh_connection=connection, transciever=transciever)
    if device_type == Router_Enum.CISCO_XR:
        interface = transciever_phy_cisco_xr(ssh_connection=connection, transciever=transciever)
    return interface




# HERE IS CISCO XR SHO OSPF NEIGHBOR DETAIL OUTPUT
# '\n
# Mon Dec 19 19:57:31.753 MST\n
# \n
# * Indicates MADJ interface\n
# # Indicates Neighbor awaiting BFD session up
# \n
# \nNeighbors for OSPF 1\n
# \n
#  Neighbor 10.225.251.253, interface address 10.225.249.245\n
#     In the area 0 via interface Bundle-Ether2 \n
#     Neighbor priority is 1, State is FULL, 6 state changes\n
#     DR is 0.0.0.0 BDR is 0.0.0.0\n    Options is 0x52  \n
#     LLS Options is 0x1 (LR)\n    Dead timer due in 00:00:36\n
#     Neighbor is up for 7w0d\n
#     Number of DBD retrans during last exchange 0\n
#     Index 1/1, retransmission queue length 0, number of retransmission 1\n
#     First 0(0)/0(0) Next 0(0)/0(0)\n
#     Last retransmission scan length is 1, maximum is 1\n
#     Last retransmission scan time is 0 msec, maximum is 0 msec\n
#     LS Ack list: NSR-sync pending 0, high water mark 0\n
# \n
# \n
# Total neighbor count: 1'