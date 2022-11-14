from fastapi import FastAPI
from actions import config_actions, netconfig_actions, csv_actions
from ssh_connector import get_connection
# from schemas.Configs import PhysicalInterface, DhcpBinding
from typing import List
from schemas.inputs import TranscieverInput

app = FastAPI()

@app.get("/")
#need to setup redirect to /docs sometime.
def read_root():
    return {"Remember": "/docs"}

@app.get("/transciever_phy_cisco_xr/")
#Get Port/tranciever information from Cisco IOS XR devices.
def get_transciever_phy_cisco_xr(transciever: str):
    print(transciever)
    ssh_connection = get_connection()
    response = config_actions.transciever_phy_cisco_xr(ssh_connection,transciever)
    ssh_connection.disconnect()
    if response == None:
        return {"status": 404, "message": "Optic not present"}
    return {"status": 202, "message": response}

@app.post("/transciever_phy_cisco_xe/")
#Get Port/tranciever information from Cisco IOS XE devices.
def get_transciever_phy_cisco_xe(transciever: TranscieverInput):
    print(transciever)
    ssh_connection = get_connection()
    response = config_actions.transciever_phy_cisco_xe(ssh_connection,transciever.tranciever)
    ssh_connection.disconnect()
    if response == None:
        return {"status": 404, "message": "Optic not present"}
    return {"status": 202, "message": response}

@app.get("/ospf_cisco_xr/")
#Get information from Cisco XR routers for the OSPF IGP protocol.
def get_ospf_cisco_xr(ospf: str):
    ssh_connection =get_connection()
    response = config_actions.ospf(ssh_connection,ospf)
    ssh_connection.disconnect
    if response:
        return({"status": 200, "message": "here you are you bugger"})
    else:
        return({"status": 404, "message": "No OSPF stats! IT IS BROKEN! Someone call Lucius!"})

# @app.get("/get_config/")
# Get router config via NETCONF.
# Future feature.
# def get_config():
#     netconfig_actions.getconfig()
#     return {"status": 202, "message": "here is the config"}

@app.post("/clear_binding/{remote_id}")
#Clear a single DHCP binding in Cisco IOS XR router.
def clear_binding(remote_id: str):
    print(remote_id)
    ssh_connection = get_connection()
    response = config_actions.clearBinding(ssh_connection,remote_id)
    ssh_connection.disconnect()
    if response:
        return({"status": 200, "message": f"Binding cleared for RSVT {remote_id}"})    
    else:
        return({"status": 404, "message": f"Binding not found for {remote_id}"})

@app.post("/clear_bindings/")
#Clear multiple DHCP binding in Cisco IOS XR router.
#This uses a csv file to input subscriber usernames
def clear_bindings():
    remote_ids = csv_actions.get_usernames()
    failed_ids = []
    ssh_connection = get_connection()
    for id in remote_ids:
        response = config_actions.clearBinding(ssh_connection,id)
        if not response:
            failed_ids.append(id)
    ssh_connection.disconnect()
    if len(failed_ids)>0:
        return({"status": 200, "message": "There were usernames with no binding present","not_bound":failed_ids})    
    else:
        return({"status": 200, "message": "All bindings cleared"})
