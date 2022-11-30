# from schemas.Configs import PhysicalInterface, DhcpBinding
from typing import List

from fastapi import BackgroundTasks, FastAPI
from fastapi.responses import RedirectResponse, JSONResponse

from actions import(
    csv_actions, 
    router_actions, 
    sevone_actions, 
    subscriber_actions, 
    save_config_actions
)
from schemas.inputs import TranscieverInput, Message
from schemas.devices import DeviceInfo, ClearBindingResponse, DeviceInfoRemoteIds
from schemas.Configs import PhysicalInterface
from ssh_connector import get_connection



app = FastAPI()


@app.get("/")
async def read_root():
    return RedirectResponse("/docs")


@app.post("/transciever_phy", response_model=PhysicalInterface, responses={202: {"model": Message}} )
def get_transciever_phy(transciever: TranscieverInput):
    """Get Port/tranciever information from Cisco IOS XE devices."""
    ssh_connection = get_connection(transciever.device_type.value, transciever.host)
    if transciever.device_type.value == "cisco_xe":
        checker = transciever.tranciever.split("/")
        if len(checker) != 3:
            return JSONResponse (
                status_code= 422,
                content= {"message": "Cisco XE transciever must be in the form of tex/x/x"}
            )
        response = router_actions.transciever_phy_cisco_xe(
            ssh_connection, transciever.tranciever
        )
        ssh_connection.disconnect()
    elif transciever.device_type.value == "cisco_xr":
        response = router_actions.transciever_phy_cisco_xr(
            ssh_connection, transciever.tranciever
        )
    if response == None:
        return JSONResponse(
            status_code = 404,
            content = "Optic not present"
        ) 
    return JSONResponse(
        status_code = 202,
        content = response.dict()
    )


@app.post("/clear_bindings", response_model= ClearBindingResponse, responses={200: {"model": ClearBindingResponse},202: {"model": ClearBindingResponse}})
def clear_binding(devices: List[DeviceInfoRemoteIds]):
    """Clear DHCP bindings in Cisco IOS XR routers."""
    clear_binding_results = ClearBindingResponse()
    for device in devices:
        ssh_connection = get_connection(device.device_type.value, device.ipAddress)
        for remote_id in device.remote_ids:
            response = subscriber_actions.clearBinding(ssh_connection, remote_id)
            if response:
                clear_binding_results.cleared.append(remote_id) 
            else:
                clear_binding_results.not_bound.append(remote_id)
        ssh_connection.disconnect()
    return JSONResponse(
        status_code = 200,
        content = clear_binding_results.dict()
    )


@app.post("/save_configs")
async def save_configs(background_tasks: BackgroundTasks):
    background_tasks.add_task(save_config_actions.save_tmarc_configs)
    return "saved"


@app.get("/device_list", response_model=List[DeviceInfo])
def device_list():
    try:
        device_list = sevone_actions.get_all_strata_devices()
        return JSONResponse(
            status_code=200,
            detail=device_list
        )
    except Exception as e:
        print(str(e))
        return JSONResponse(
            status_code=500,
            detail=str(e)
        )


@app.get("/ospf_cisco_xr/")
def get_ospf_cisco_xr(ospf: str):
    """Get information from Cisco XR routers for the OSPF IGP protocol."""
    ssh_connection = get_connection()
    response = router_actions.ospf(ssh_connection, ospf)
    ssh_connection.disconnect()
    if response:
        return {"status": 200, "message": "here you are you bugger"}
    else:
        return {
            "status": 404,
            "message": "No OSPF stats! IT IS BROKEN! Someone call Lucius!",
        }


# @app.get("/get_config/")
# Get router config via NETCONF.
# Future feature.
# def get_config():
#     netconfig_actions.getconfig()
#     return {"status": 202, "message": "here is the config"}




"""  "message": [
    {
      "id": 162,
      "isDeleted": false,
      "isNew": false,
      "name": "vrnl-cp-250-state-dnr-office",
      "alternateName": "vrnl-cp-250-state-dnr-office",
      "description": "STRATA Networks",
      "ipAddress": "10.229.32.122",
      "manualIP": false,
      "peerId": 1,
      "pollFrequency": 300,
      "dateAdded": 1455321241000,
      "lastDiscovery": 1669532417000,
      "allowDelete": true,
      "disablePolling": false,
      "disableConcurrentPolling": false,
      "disableThresholding": false,
      "timezone": "America/Denver",
      "workhoursGroupId": 1,
      "numElements": 5,
      "pluginInfo": null,
      "objects": null,
      "pluginManagerId": null
    },
    {
      "id": 164,
      "isDeleted": false,
      "isNew": false,
      "name": "ftbt-cp-280-uen-myton",
      "alternateName": "UEN Myton",
      "description": "STRATA Networks",
      "ipAddress": "10.229.16.101",
      "manualIP": false,
      "peerId": 1,
      "pollFrequency": 300,
      "dateAdded": 1455321241000,
      "lastDiscovery": 1669532418000,
      "allowDelete": true,
      "disablePolling": false,
      "disableConcurrentPolling": false,
      "disableThresholding": false,
      "timezone": "America/Denver",
      "workhoursGroupId": 1,
      "numElements": 5,
      "pluginInfo": null,
      "objects": null,
      "pluginManagerId": null
    },"""


""" this is xe
    lab-cr-903-1#show hw-module subslot 0/0 transceiver 0 status
The Transceiver in slot 0 subslot 0 port 0 is enabled.
  Module temperature                        = +52.000 C
  Transceiver Tx supply voltage             = 3212.0 mVolts
  Transceiver Tx bias current               = 37920 uAmps
  Transceiver Tx power                      = -3.3 dBm
  Transceiver Rx optical power              = -0.9 dBm




lab-cr-903-1#show hw-module subslot 0/0 transceiver 0 idprom
IDPROM for transceiver TenGigabitEthernet0/0/0:
  Description                               = SFP+ optics (type 130)
  Transceiver Type:                         = SFP+ 10GBASE-LR (274)
  Product Identifier (PID)                  = SFP-10G-LR
  Vendor Revision                           = V03
  Serial Number (SN)                        = N098520AG875
  Vendor Name                               = OEM
  Vendor OUI (IEEE company ID)              = 20.20.20 (2105376)
  CLEI code                                 = SFP+LR
  Cisco part number                         =
  Device State                              = Enabled.
  Date code (yy/mm/dd)                      = 20/01/16
  Connector type                            = LC.
  Encoding                                  = 64B66B
  Nominal bitrate                           = 10GE (10300 Mbits/s)
  Minimum bit rate as % of nominal bit rate = not specified
  Maximum bit rate as % of nominal bit rate = not specified
lab-cr-903-1#
"""



"""this is xr
RP/0/RSP0/CPU0:lab-ac-9006#show controllers tenGigE0/0/0/0 all
Sun Nov 27 21:41:31.806 MST
Operational data for interface TenGigE0/0/0/0:

State:
    Administrative state: enabled
    Operational state: Up
    LED state: Green On

Phy:
    Media type: R fiber over 1310nm optics
    Optics:
        Vendor: CISCO-FINISAR
        Part number: FTLX1474D3BCL-CS
        Serial number: FNS16100CQX
        Type: SFP-10G-LR
        Rev: A
        Wavelength: 1310 nm
    Digital Optical Monitoring:
        Transceiver Temp: 27.562 C
        Transceiver Voltage: 3.348 V

        DOM alarms:
            No alarms

        Alarm                     Alarm    Warning   Warning    Alarm
        Thresholds                High      High       Low       Low
                                 -------   -------   -------   -------
        Transceiver Temp (C):     75.000    70.000     0.000    -6.000
        Transceiver Voltage (V):   3.700     3.600     3.000     2.900
        Laser Bias (mA):          85.000    80.000    20.000    15.000
        Transmit Power (mW):       2.237     1.120     0.151     0.060
        Transmit Power (dBm):      3.497     0.492    -8.210   -12.218
        Receive Power (mW):        2.237     1.120     0.036     0.014
        Receive Power (dBm):       3.497     0.492   -14.437   -18.539

MAC address information:
    Operational address: 5087.8972.68c4
    Burnt-in address: 8478.ac7f.1804
    No unicast addresses in filter
    No multicast addresses in filter

Autonegotiation disabled.

Operational values:
    Speed: 10Gbps
    Duplex: Full Duplex
    Flowcontrol: None
    Loopback: None (or external)
    MTU: 9216
    MRU: 9216
    Inter-packet gap: standard (12)

BERT status for TenGigE0/0/0/0:

BERT State                      :       DISABLED
Test Pattern                    :       None test pattern
Time Remaining                  :       0
Time Interval                   :       0
Statistics for interface TenGigE0/0/0/0 (cached values):

Ingress:
    Input total bytes           = 12787710042
    Input good bytes            = 12787710042

    Input total packets         = 67114942
    Input 802.1Q frames         = 0
    Input pause frames          = 0
    Input pkts 64 bytes         = 314009
    Input pkts 65-127 bytes     = 59586850
    Input pkts 128-255 bytes    = 835228
    Input pkts 256-511 bytes    = 794013
    Input pkts 512-1023 bytes   = 97368
    Input pkts 1024-1518 bytes  = 392114
    Input pkts 1519-Max bytes   = 5095360

    Input good pkts             = 67114942
    Input unicast pkts          = 66108263
    Input multicast pkts        = 1006611
    Input broadcast pkts        = 68

    Input drop overrun          = 0
    Input drop abort            = 0
    Input drop invalid VLAN     = 0
    Input drop invalid DMAC     = 0
    Input drop invalid encap    = 0
    Input drop other            = 0

    Input error giant           = 0
    Input error runt            = 0
    Input error jabbers         = 0
    Input error fragments       = 0
    Input error CRC             = 0
    Input error collisions      = 0
    Input error symbol          = 0
    Input error other           = 0

    Input MIB giant             = 5095360
    Input MIB jabber            = 0
    Input MIB CRC               = 0

Egress:
    Output total bytes          = 137900858282
    Output good bytes           = 137900858282

    Output total packets        = 115578750
    Output 802.1Q frames        = 0
    Output pause frames         = 0
    Output pkts 64 bytes        = 60691
    Output pkts 65-127 bytes    = 8259988
    Output pkts 128-255 bytes   = 3555737
    Output pkts 256-511 bytes   = 6852763
    Output pkts 512-1023 bytes  = 13754947
    Output pkts 1024-1518 bytes = 11205785
    Output pkts 1519-Max bytes  = 71888839

    Output good pkts            = 115578750
    Output unicast pkts         = 42746986
    Output multicast pkts       = 942924
    Output broadcast pkts       = 1

    Output drop underrun        = 0
    Output drop abort           = 0
    Output drop other           = 0

    Output error other          = 0

Management information for interface TenGigE0/0/0/0:

Bay number: 0
Port number: 0
Interface handle: 0x40000c0

Config:
    Auto-negotiation: Configuration not supported (Off)
    Carrier delay (up): Not configured
    Carrier delay (down): Not configured
    Speed: Configuration not supported (10Gbps)
    Duplex: Configuration not supported (Full Duplex)
    Flow Control: Not configured (None)
    Priority Flow Control: Configuration not supported
    Forward Error Correction: Configuration not supported
    IPG: Not configured (standard (12))
    Loopback: Not configured (None)
    MTU: Not configured
    Bandwidth: Not configured
    BER-SD Threshold: Configuration not supported
    BER-SD Report: Configuration not supported
    BER-SF Threshold: Configuration not supported
    BER-SF Report: Configuration not supported
    BER-SF Signal Remote Failure: Configuration not supported
    Rx Optical Power Degrade Threshold: Not configured (51)
    Fast Shutdown: Not configured (Not configured globally)

Driver constraints:
    Min MTU: 64 bytes
    Max MTU: 9216 bytes
    Max speed: 10Gbps
    Interface type: TenGigE
    Management interface: No
    Promiscuous mode: Yes
    Default carrier delay up (auto-neg on): 10 ms
    Default carrier delay down (auto-neg on): 0 ms
    Default carrier delay up (auto-neg off): 10 ms
    Default carrier delay down (auto-neg off): 0 ms
    Default carrier delay down (tx enable): 1000 ms
    Allowed config mask: 0x427b
    Min Rx Optical Power Degrade Threshold: -300
    Max Rx Optical Power Degrade Threshold: 50
    BER:
        SD (min - max): (1e-6 - 1e-9)
        SD default: 1e-8
        SF (min - max): (1e-6 - 1e-9)
        SF default: 1e-6

Cached driver state:
    MTU: 9216 bytes
    Burnt-in MAC address: 8478.ac7f.1804

Operational carrier delay:
    Carrier delay (up): 10 ms
    Carrier delay (down): 0 ms

Bundle settings:
    Bundle interface: Bundle-Ether2
    Bundle MTU: 9216 bytes
    Bundle MAC address: 5087.8972.68c4

Satellite uplink settings:
    Not in satellite uplink (ICL) mode.

Port FSM state:
    Port is enabled, link is up

Complete FSM state:
    Admin up
 --More-- filtering...
        SF default: 1e-6

Cached driver state:
    MTU: 9216 bytes
    Burnt-in MAC address: 8478.ac7f.1804

Operational carrier delay:
    Carrier delay (up): 10 ms
    Carrier delay (down): 0 ms

Bundle settings:
    Bundle interface: Bundle-Ether2
    Bundle MTU: 9216 bytes
    Bundle MAC address: 5087.8972.68c4

Satellite uplink settings:
    Not in satellite uplink (ICL) mode.

Port FSM state:
    Port is enabled, link is up

Complete FSM state:
    Admin up
    Client admin up
    Client admin tx not disabled
    Port enabled
    Port tx enabled
    Hardware link up
IDB interface state information:
    IDB client admin up
    IDB client tx admin up
    IDB error disable not set

0 Unicast MAC Addresses:

0 Multicast MAC Addresses:

0 Unicast Bundle MAC Addresses:


Link faults for interface: TenGigE0/0/0/0
 none

Internal data for interface: TenGigE0/0/0/0
Port Number         : 0
Bay Number          : 0
Ifinst              : 0
Ifinst Subport      : 0
Board Type          : 0x00390260
Port Type           : 10GE
Bandwidth(Kbps)     : 10000000
Transport mode      : LAN
BIA MAC addr        : 8478.ac7f.1804
Oper. MAC addr      : 5087.8972.68c4
Egress MAC addr     : 5087.8972.68c4
Port Available      : true
Status polling is   : enabled
Status events are   : enabled
I/F Handle          : 0x040000c0
Cfg Link Enabled    : tx/rx enabled
H/W Tx Enable       : yes
MTU                 : 9216
H/W Speed           : 10 Gbps
H/W Duplex          : Full
H/W Loopback Type   : None
FEC                 : Disable
H/W FlowCtrl Type   : None
H/W AutoNeg Enable  : Off
Rx OPD              : Disabled
H/W Link Defects    : (0x0000000000000000)  none
H/W Raw Link Defects : (0x0000000000000000)  none
Link Up             : yes
Link Led Status     : Link up   -- Green/Amber
Serdes hw version   : 0.3
Serdes sw version   : 8.0
Pluggable Present   : yes
Pluggable Type      : SFP-10G-LR
Pluggable PID       : SFP-10G-LR
Pluggable Compl.    : (Service Un) - Compliant
Pluggable Type Supp.: (Service Un) - Supported
Pluggable PID Supp. : (Service Un) - Supported

PHY data for interface: TenGigE0/0/0/0

SFP EEPROM  port: 0
        Xcvr Type: SFP
        Xcvr Code: SFP-10G-LR
        Encoding: 64B66B
        Bit Rate: 10300 Mbps
        Link Reach 9u fiber (Km): 10000 meter
        Link Reach 9u fiber (100m): 10000 meter
        Vendor Name: CISCO-FINISAR
        Vendor OUI: 00.90.65
        Vendor Part Number: FTLX1474D3BCL-CS (rev.: A   )
        Laser wavelength: 1310 nm (fraction: 0.00 nm)
        Optional SFP Signal: Tx_Disable, Tx_Fault, LOS
        Vendor Serial Number: FNS16100CQX
        Date Code (yy/mm/dd): 12/03/05  lot code:
        Diagnostic Monitoring: DOM, Int. Cal.,
        Enhanced Options: SW TX Fault Mon, SW TX Disable, Alarm/Warning Flags

MSA Data
0x0000: 03 04 07 20 00 00 00 00 : 00 00 00 06 67 00 0a 64
0x0010: 00 00 00 00 43 49 53 43 : 4f 2d 46 49 4e 49 53 41
0x0020: 52 20 20 20 00 00 90 65 : 46 54 4c 58 31 34 37 34
0x0030: 44 33 42 43 4c 2d 43 53 : 41 20 20 20 05 1e 00 e5
0x0040: 00 1a 00 00 46 4e 53 31 : 36 31 30 30 43 51 58 20
0x0050: 20 20 20 20 31 32 30 33 : 30 35 20 20 68 e0 03 3b
0x0060: 00 00 08 3f 08 4c 5b 62 : e7 e4 42 07 70 04 05 ed
0x0070: 01 75 8c 65 8b 00 00 00 : 00 00 60 07 c7 f1 20 7d

        Thresholds:                    Alarm High         Warning High          Warning Low            Alarm Low
              Temperature:            +75.000 C             +70.000 C              +0.000 C              -6.000 C
                  Voltage:           3.700 Volt            3.600 Volt            3.000 Volt            2.900 Volt
                     Bias:         85.000 mAmps          80.000 mAmps          20.000 mAmps          15.000 mAmps
           Transmit Power:  2.23720 mW (3.49705 dBm)   1.12080 mW (0.49528 dBm)   0.15150 mW (-8.19587 dBm)   0.06020 mW (-12.20404 dBm)
            Receive Power:  2.23720 mW (3.49705 dBm)   1.12080 mW (0.49528 dBm)   0.03630 mW (-14.40093 dBm)   0.01440 mW (-18.41638 dBm)
        Temperature: 27.563
        Voltage: 3.349 Volt
        Tx Bias: 30.938 mAmps
        Tx Power:  0.62330 mW (-2.05303 dBm)
        Rx Power:  0.50910 mW (-2.93197 dBm)
        Oper. Status/Control:
EEPROM Memory (A2 lower)
0x0100: 4b 00 fa 00 46 00 00 00 : 90 88 71 48 8c a0 75 30
0x0110: a6 04 1d 4c 9c 40 27 10 : 57 64 02 5a 2b c8 05 eb
0x0120: 57 64 00 90 2b c8 01 6b : 00 00 00 00 00 00 00 00
0x0130: 00 00 00 00 00 00 00 00 : 00 00 00 00 00 00 00 00
0x0140: 00 00 00 00 3f 80 00 00 : 00 00 00 00 01 00 00 00
0x0150: 01 00 00 00 01 00 00 00 : 01 00 00 00 00 00 00 ba
0x0160: 1b 90 82 cd 3c 6d 18 59 : 13 e3 ff ff ff ff 00 ff
0x0170: 00 3f ff ff 00 3f ff ff : ff ff ff 00 00 00 00 01

        CLEI Code: COUIA75CAA
        Part Number: 10-2457-02 (ver.: V02 )
        Temp/Alarm/Power Flags: COM, commercial 0C to 70C
        Minimum Temperature: 0
        Maximum Temperature: 70
        Calibration Constants: LBC Scale, Temperature, Laser bias current, Output power,
        Product Id: SFP-10G-LR
EEPROM Memory (A2 upper)
0x0180: 43 4f 55 49 41 37 35 43 : 41 41 31 30 2d 32 34 35
0x0190: 37 2d 30 32 56 30 32 20 : 01 00 46 00 00 00 00 b0
0x01a0: 00 00 00 00 00 00 00 00 : 00 00 8c dd 94 00 ac a5
0x01b0: d6 cd 00 00 1e 00 57 93 : 17 0c 0f 2b 00 00 aa aa
0x01c0: 53 46 50 2d 31 30 47 2d : 4c 52 20 20 20 20 20 20
0x01d0: 20 20 20 20 32 33 00 00 : 00 00 00 00 00 00 00 2e
0x01e0: 20 26 2b 30 33 36 2b 36 : 00 00 00 00 00 00 00 00
0x01f0: 00 00 00 00 00 6b 00 00 : ff ff ff ff 00 00 00 00



Port status: TenGigE0/0/0/0
  OPTICS:
   Rx LOS Fault       : No
   Tx Fault           : No

  PHY:
   Tx Align Fault     : No
   PMA/PMD:
    Rx LOS Fault      : No
    Rx PMA link Fault : No
   PCS:
    Rx PCS link Fault : No
    Rx PCS lock Fault : No

  MAC:
   Rx Local Fault     : No
   Rx Remote Fault    : No



Registers for interface: TenGigE0/0/0/0
AFP registers:
0x0000 afp_ctl_reg_info                        : 0x002c1441
0x0004 afp_ctl_reg_init_stat                   : 0x00000000
0x0008 afpctl_reg                              : 0x00000011
0x000c afpstat_reg                             : 0x00000000
0x0010 afpint_reg                              : 0x00000000
0x0014 afpmask_reg                             : 0x00000008
0x0018 afpint_frc_reg                          : 0x00000000
Silab Status:
0x0000 SILABS_PLL_STATUS                       : 0x00000000
Serdes registers:
0x0000 TOP: CHIP_DEV_ID                        : 0x0000eac5
0x0000 TOP: CHIP_DEV_VER                       : 0x00000003
0x0000 RX: PCS_HIBER_CNT_NR                    : 0x00000000
0x0000 RX: PCS_BLKERR_CNT_NR                   : 0x00000000
0x0000 RX: HI_BER_LH                           : 0x00000000
0x0000 RX: PCS_RXLINK_STAT                     : 0x00000001
0x0000 RX: BLOCK_LOCK_LL                       : 0x00000001
0x0000 RX: HSIFBu_GR_RLD_LOCKDET               : 0x00000001
0x0000 RX: XG_REMOTE_FAULT                     : 0x00000000
0x0000 TX: HSIFBu_GC_RLD_LOCKDET               : 0x00000001
0x0000 RX: HSIFAu_GR_RLD_LOCKDET               : 0x00000000
0x0000 TX: HSIFAu_GC_RLD_LOCKDET               : 0x00000000
0x0000 TX: LANE_ALIGN                          : 0x00000001
0x0000 TX: LANE_SYNC                           : 0x0000000f
0x0000 TX: XG_NO_FRAME_LOCK                    : 0x00000001
0x0000 TX: XG_HI_BER                           : 0x00000000
0x0000 TX: XG_LINK_STATUS                      : 0x00000000
0x0000 TX: XG_LOCAL_FAULT                      : 0x00000000
0x0000 TX: XG_REMOTE_FAULT                     : 0x00000000
0x0000 TX: XCDR_ERR_CNT_NR_0                   : 0x00000000
0x0000 TX: XCDR_ERR_CNT_NR_1                   : 0x00000000
0x0000 TX: XCDR_ERR_CNT_NR_2                   : 0x00000000
0x0000 TX: XCDR_ERR_CNT_NR_3                   : 0x00000000
RP/0/RSP0/CPU0:lab-ac-9006#
"""