class Ospf:
    __slots__=[
        "neighbor",
        "interface_address",
        "area",
        "interface",
        "neighbor_priority",
        "state",
        "state_changes",
        "designated_router",
        "backup_designated_router",
        "dead_timer",
        "neighbor_uptime",
        "database_description_retransmission",
        "index",
        "retransmission_queue_length",
        "retansmission_number",
        "last_retransmission_scan_length",
        "total_neighbor_count"
    ]

def __init__(
    self,
    neighbor= None,
    interface_address= None,
    area= None,
    interface= None,
    neighbor_priority= None,
    state= None,
    state_changes= None,
    designated_router= None,
    backup_designated_router= None,
    dead_timer= None,
    neighbor_uptime= None,
    database_description_retransmission= None,
    index= None,
    retransmission_queue_length= None,
    retansmission_number= None,
    last_retransmission_scan_length= None,
    total_neighbor_count= None
):
    self.neighbor = neighbor
    self.interface_address = interface_address
    self.area = area
    self.interface = interface
    self.neighbor_priority = neighbor_priority
    self.state = state
    self.state_changes = state_changes
    self.designated_router = designated_router
    self.backup_designated_router = backup_designated_router
    self.dead_timer = dead_timer
    self.neighbor_uptime = neighbor_uptime
    self.database_description_retransmission = database_description_retransmission
    self.index = index
    self.retransmission_queue_length = retransmission_queue_length
    self.retansmission_number = retansmission_number
    self.last_retransmission_scan_length = last_retransmission_scan_length
    self.total_neighbor_count = total_neighbor_count