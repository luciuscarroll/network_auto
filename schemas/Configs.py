from pydantic import BaseModel

class DhcpBinding(BaseModel):
    mac_address: str | None
    vrf: str | None
    ip_address: str | None
    server_vrf: str | None
    giaddr_from_client: str | None
    giaddr_to_server: str | None
    server_ip_address_to_client: str | None
    server_ip_address: str | None
    received_circuit_id: str | None
    insert_circuit_id: str | None
    received_remote_id: str | None
    inserted_remote_id: str | None
    recieved_VSISO: str | None
    inserted_VSISO: str | None
    Auth_on_recieved_relay: str | None
    param_request_option: str | None
    saved_options: str | None
    profile: str | None
    state: str | None
    lease: str | None
    lease_remaining: str | None
    client_id: str | None
    access_interface: str | None
    access_vrf: str | None
    subsriber_label: str | None
    srg_state: str | None
    event_history: str | None
    session_start: str | None
    packet_discover: str | None
    dpm_success: str | None
    packet_offer: str | None
    packet_request: str | None
    packet_ack: str | None
    lease_dpm_success: str | None
    route_success: str | None

class PhysicalInterface(BaseModel):
    transciever_type: str | None
    transciever_part_number: str | None
    laser_wavelength: str | None
    transmit_power: str | None
    recieve_power: str | None
    vendor_name: str | None
    interface: str | None
    admin_state: str | None

class OSPF(BaseModel):
    neighbor: str | None
    interface_address: str | None
    area: str | None
    interface: str | None
    neighbor_priority: str | None
    state: str | None
    up_time: str | None
    state_changes: str | None
    designated_router: str | None
    backup_designated_router: str | None
    dead_timer: str | None
    neighbor_uptime: str | None
    database_description_retransmission: str | None
    index: str | None
    retransmission_queue_length: str | None
    retansmission_number: str | None
    last_retransmission_scan_length: str | None
    total_neighbor_count: str | None