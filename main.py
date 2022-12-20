import os
from fastapi import BackgroundTasks, FastAPI, Response, status
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from actions import (
    router_actions,
    sevone_actions,
    subscriber_actions,
)
from schemas.inputs import Router_Enum, Message
from schemas.devices import DeviceInfo, ClearBindingResponse, DeviceInfoRemoteIds, SevoneGroup
from schemas.Configs import PhysicalInterface, OSPF
from ssh_connector import get_connection

load_dotenv()
app = FastAPI()



@app.get("/")
async def read_root():
    return RedirectResponse("/docs")


@app.get(
    "/transciever_phy",
    responses={202: {"model": PhysicalInterface},404: {"model": Message}, 422: {"model": Message}},
    status_code=202
)
def get_transciever_phy(transciever: str, host: str, device_type: Router_Enum, response: Response):
    """Get transciever information from Cisco devices."""
    try:
        checker = [int(x) for x in transciever.split("/")]
    except ValueError as e:        
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return Message(message="Transceiver must contain only numbers and /'s")
    if device_type == Router_Enum.CISCO_XE and len(checker)  != 3:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return Message(message="Cisco XE transciever must be in the form of x/x/x")
    if device_type == Router_Enum.CISCO_XR and len(checker) != 4:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return Message(message="Cisco XR transciever must be in the form of x/x/x/x")
    ssh_connection = get_connection(device_type.value, host)
    interface = router_actions.get_physical_interface(connection=ssh_connection, transciever=transciever, device_type=device_type)
    ssh_connection.disconnect()
    if interface == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return Message(message=f"Optic not present for transciever te{transciever}")
    return interface


@app.get(
    "/ospf/",
    responses={202:{"model": list[OSPF]},404: {"model": Message}},
    status_code=202
)
def get_ospf(response: Response):
    """Get information from routers for the OSPF IGP protocol."""
    # TODO make ssh connection dynamic from front end.
    # TODO rework reponses.
    ssh_connection = get_connection(device_type="cisco_xr", host = os.getenv("LAB_HOST"))
    ospf_details = router_actions.ospf_neighbor_cisco_xr(ssh_connection)
    ssh_connection.disconnect()
    if ospf_details == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return Message(message=f"No OSPF neighbors found.")
    return ospf_details



@app.post(
    "/clear_bindings",
    responses={
        200: {"model": ClearBindingResponse}
    },
)
def clear_binding(devices: list[DeviceInfoRemoteIds]):
    """Clear DHCP bindings in Cisco IOS XR routers."""
    clear_binding_results = ClearBindingResponse()
    for device in devices:
        ssh_connection = get_connection(device.device_type.value, device.ipAddress)
        for remote_id in device.remote_ids:
            did_clear = subscriber_actions.clearBinding(ssh_connection, remote_id)
            if did_clear:
                clear_binding_results.cleared.append(remote_id)
            else:
                clear_binding_results.not_bound.append(remote_id)
        ssh_connection.disconnect()
    return clear_binding_results


@app.get(
    "/group_list",
    responses={200: {"model": list[SevoneGroup]}, 408: {"model": Message}, 500: {"model": Message}},
)
def get_group_list(
    response: Response
):
    try:
        group_list = sevone_actions.sevone_group_list()
        return group_list
    except TimeoutError as e:
        print(str(e))
        response.status_code=status.HTTP_408_REQUEST_TIMEOUT
        return Message(message="Sevone was not reachable. Please try again.")
    except Exception as e:
        print(str(e))
        response.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        return Message(message=str(e))


@app.get(
    "/device_list{group_id}",
    responses={200: {"model": list[DeviceInfo]}, 408: {"model": Message}, 500: {"model": Message}},
)
def device_list(
    group_id: int,
    response: Response
):
    try:
        device_list = sevone_actions.sevone_device_list(group_id)
        return device_list
    except TimeoutError as e:
        print(str(e))
        response.status_code=status.HTTP_408_REQUEST_TIMEOUT
        return Message(message="Sevone was not reachable. Please try again.")
    except Exception as e:
        print(str(e))
        response.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        return Message(message=str(e))


@app.get("/test")
def test():
    sevone_actions.get_all_tmarcs()
    return {"message": "Test Complete"}


# @app.get("/get_config/")
# Get router config via NETCONF.
# Future feature.
# def get_config():
#     netconfig_actions.getconfig()
#     return {"status": 202, "message": "here is the config"}
