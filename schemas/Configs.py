from typing import Optional
from pydantic import BaseModel

class DhcpBinding(BaseModel):
    mac_address: Optional[str] = None
    vrf: Optional[str] = None
    ip_address: Optional[str] = None
    server_vrf: Optional[str] = None
    giaddr_from_client: Optional[str] = None
    giaddr_to_server: Optional[str] = None
    server_ip_address_to_client: Optional[str] = None
    server_ip_address: Optional[str] = None
    received_circuit_id: Optional[str] = None
    insert_circuit_id: Optional[str] = None
    received_remote_id: Optional[str] = None
    inserted_remote_id: Optional[str] = None
    recieved_VSISO: Optional[str] = None
    inserted_VSISO: Optional[str] = None
    Auth_on_recieved_relay: Optional[str] = None
    param_request_option: Optional[str] = None
    saved_options: Optional[str] = None
    profile: Optional[str] = None
    state: Optional[str] = None
    lease: Optional[str] = None
    lease_remaining: Optional[str] = None
    client_id: Optional[str] = None
    access_interface: Optional[str] = None
    access_vrf: Optional[str] = None
    subsriber_label: Optional[str] = None
    srg_state: Optional[str] = None
    event_history: Optional[str] = None
    session_start: Optional[str] = None
    packet_discover: Optional[str] = None
    dpm_success: Optional[str] = None
    packet_offer: Optional[str] = None
    packet_request: Optional[str] = None
    packet_ack: Optional[str] = None
    lease_dpm_success: Optional[str] = None
    route_success: Optional[str] = None

class PhysicalInterface(BaseModel):
    transciever_type: Optional[str] = None
    transciever_part_number: Optional[str] = None
    laser_wavelength: Optional[str] = None
    transmit_power: Optional[str] = None
    recieve_power: Optional[str] = None
    vendor_name: Optional[str] = None
    interface: Optional[str] = None
    admin_state: Optional[str] = None

class OSPF(BaseModel):
    neighbor_id: Optional[str] = None
    area: Optional[str] = None
    state: Optional[str] = None
    up_time: Optional[str] = None