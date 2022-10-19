import imp
from urllib import response
from fastapi import FastAPI
from actions import config_actions
from ssh_connector import get_connection

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
    return response


@app.get("/transciever_phy/")
def get_transciever_phy(transciever: str):
    print(transciever)
    ssh_connection = get_connection()
    response = config_actions.transciever_phy(ssh_connection,transciever)
    ssh_connection.disconnect()
    return response
