class PhysicalInterface:
    __slots__=[
        "module_temperature",
        "transciever_voltage",
        "transciever_tx_bias_current",
        "transciever_tx_power",
        "transciever_rx_optical_power",
        "description",
        "transciever_type",
        "product_identifier",
        "vendor_revision",
        "serial_number",
        "vendor_name",
        "vendor_oui",
        "clei_code",
        "cisco_part_number",
        "device_state",
        "date_code",
        "connector_type",
        "encoding",
        "nominal_bitrate",
        "minimum_bitrate",
        "maximum_bitrate",
        "interface"
    ]

    def __init__(
        self,
        module_temperature= None,
        transciever_voltage= None,
        transciever_tx_bias_current= None,
        transciever_tx_power= None,
        transciever_rx_optical_power= None,
        description= None,
        transciever_type= None,
        product_identifier= None,
        vendor_revision= None,
        serial_number= None,
        vendor_name= None,
        vendor_oui= None,
        clei_code= None,
        cisco_part_number= None,
        device_state= None,
        date_code= None,
        connector_type= None,
        encoding= None,
        nominal_bitrate= None,
        minimum_bitrate= None,
        maximum_bitrate= None,
        interface= None
    ):
        self.module_temperature = module_temperature
        self.transciever_voltage = transciever_voltage
        self.transciever_tx_bias_current = transciever_tx_bias_current
        self.transciever_tx_power = transciever_tx_power
        self.transciever_rx_optical_power = transciever_rx_optical_power
        self.description = description
        self.transciever_type = transciever_type
        self.product_identifier = product_identifier
        self.vendor_revision = vendor_revision
        self.serial_number = serial_number
        self.vendor_name = vendor_name
        self.vendor_oui = vendor_oui
        self.clei_code = clei_code
        self.cisco_part_number = cisco_part_number
        self.device_state = device_state
        self.date_code = date_code
        self.connector_type = connector_type
        self.encoding = encoding
        self.nominal_bitrate = nominal_bitrate
        self.minimum_bitrate = minimum_bitrate
        self.maximum_bitrate = maximum_bitrate
        self.interface = interface
