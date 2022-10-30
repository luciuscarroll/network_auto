from pickle import EMPTY_LIST
from fastapi import FastAPI
from actions import config_actions, netconfig_actions, csv_actions
from ssh_connector import get_connection
from schemas.Configs import PhysicalInterface, DhcpBinding
from typing import List


app = FastAPI()


@app.get("/")
def read_root():
    return {"Remember": "/docs"}


@app.post("/clear_binding/{remote_id}")
def clear_binding(remote_id: str):
    print(remote_id)
    ssh_connection = get_connection()
    response = config_actions.clearBinding(ssh_connection,remote_id)
    ssh_connection.disconnect()
    if response:
        return({"status": 200, "message": f"Binding cleared for RSVT {remote_id}"})    
    else:
        return({"status": 404, "message": f"Binding not found for {remote_id}"})


@app.get("/transciever_phy/")
def get_transciever_phy(transciever: str):
    print(transciever)
    ssh_connection = get_connection()
    response = config_actions.transciever_phy(ssh_connection,transciever)
    ssh_connection.disconnect()
    if response == None:
        return {"status": 404, "message": "Optic not present"}
    return {"status": 202, "message": response}


@app.get("/get_config/")
def get_config():
    netconfig_actions.getconfig()
    return {"status": 202, "message": "here is the config"}



@app.post("/clear_bindings/")
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



