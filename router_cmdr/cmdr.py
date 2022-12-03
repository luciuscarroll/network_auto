from netmiko import ConnectHandler
import cisco_xr

def connect(device_type, host, username, password):
    """Returns a netmiko SSH session"""
    ssh_session = ConnectHandler(
        device_type=device_type, host=host, username=username, password=password
    )
    return ssh_session

def disconnect(connection):
    """Disconnects SSH session"""
    connection.disconnect()

def cisco_xr_tranciever_phy(connection, transciever):
    r
