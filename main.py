# from schemas.Configs import PhysicalInterface, DhcpBinding
from typing import List

from fastapi import BackgroundTasks, FastAPI
from fastapi.responses import RedirectResponse

from actions import csv_actions, router_actions, sevone_actions, subscriber_actions, save_config_actions
from schemas.inputs import TranscieverInput
from ssh_connector import get_connection

app = FastAPI()


@app.get("/")
async def read_root():
    return RedirectResponse("/docs")

#TODO combine with xe function and change input to accept router type.

@app.get("/transciever_phy_cisco_xr/")
def get_transciever_phy_cisco_xr(transciever: str):
    """Get Port/tranciever information from Cisco IOS XR devices."""
    print(transciever)
    ssh_connection = get_connection()
    response = router_actions.transciever_phy_cisco_xr(ssh_connection, transciever)
    ssh_connection.disconnect()
    if response == None:
        return {"status": 404, "message": "Optic not present"}
    return {"status": 202, "message": response}


@app.post("/transciever_phy_cisco_xe/")
def get_transciever_phy_cisco_xe(transciever: TranscieverInput):
    """Get Port/tranciever information from Cisco IOS XE devices."""
    print(transciever)
    ssh_connection = get_connection()
    response = router_actions.transciever_phy_cisco_xe(
        ssh_connection, transciever.tranciever
    )
    ssh_connection.disconnect()
    if response == None:
        return {"status": 404, "message": "Optic not present"}
    return {"status": 202, "message": response}


@app.get("/ospf_cisco_xr/")
def get_ospf_cisco_xr(ospf: str):
    """Get information from Cisco XR routers for the OSPF IGP protocol."""
    ssh_connection = get_connection()
    response = router_actions.ospf(ssh_connection, ospf)
    ssh_connection.disconnect
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


@app.post("/clear_binding/{remote_id}")
def clear_binding(remote_id: str):
    """Clear a single DHCP binding in Cisco IOS XR router."""
    print(remote_id)
    ssh_connection = get_connection()
    response = subscriber_actions.clearBinding(ssh_connection, remote_id)
    ssh_connection.disconnect()
    if response:
        return {"status": 200, "message": f"Binding cleared for RSVT {remote_id}"}
    else:
        return {"status": 404, "message": f"Binding not found for {remote_id}"}


@app.post("/clear_bindings/")
def clear_bindings():
    """Clear multiple DHCP binding in Cisco IOS XR router."""
    remote_ids = csv_actions.get_usernames()
    failed_ids = []
    ssh_connection = get_connection()
    for id in remote_ids:
        response = subscriber_actions.clearBinding(ssh_connection, id)
        if not response:
            failed_ids.append(id)
    ssh_connection.disconnect()
    if len(failed_ids) > 0:
        return {
            "status": 200,
            "message": "There were usernames with no binding present",
            "not_bound": failed_ids,
        }
    else:
        return {"status": 200, "message": "All bindings cleared"}


@app.post("/save_configs")
async def save_configs(background_tasks: BackgroundTasks):
    background_tasks.add_task(save_config_actions.save_tmarc_configs)
    return "saved"


@app.get("/device_list")
def device_list():
    device_list = sevone_actions.sevone_device_list()
    return {
        "status": 200,
        "message": device_list
    }

