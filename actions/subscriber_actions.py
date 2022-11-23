from schemas.Configs import DhcpBinding


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
    if binding_details.mac_address:
        ssh_connection.send_command(f"clear dhcp ipv4 proxy binding mac-address {binding_details.mac_address}")
        return True    
    else:
        return False
