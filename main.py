from fastapi import BackgroundTasks, FastAPI, Response, status
from fastapi.responses import RedirectResponse

from actions import (
    router_actions,
    sevone_actions,
    subscriber_actions,
)
from schemas.inputs import Router_Enum, Message
from schemas.devices import DeviceInfo, ClearBindingResponse, DeviceInfoRemoteIds, SevoneGroup
from schemas.Configs import PhysicalInterface
from ssh_connector import get_connection


app = FastAPI()


@app.get("/")
async def read_root():
    return RedirectResponse("/docs")


@app.get(
    "/transceiver_phy",
    responses={202: {"model": PhysicalInterface},404: {"model": Message}, 422: {"model": Message}},
    status_code=202
)
def get_transceiver_phy(transceiver: str, host: str, device_type: Router_Enum, response: Response):
    """Get transceiver information from Cisco devices."""
    try:
        checker = [int(x) for x in transceiver.split("/")]
    except ValueError as e:        
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return Message(message="Transceiver must contain only numbers and /'s")
    if device_type == Router_Enum.CISCO_XE and len(checker)  != 3:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return Message(message="Cisco XE transceiver must be in the form of x/x/x")
    if device_type == Router_Enum.CISCO_XR and len(checker) != 4:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return Message(message="Cisco XR transceiver must be in the form of x/x/x/x")
    # ssh_connection = "get_connection(device_type.value, host)"
    ssh_connection = get_connection(device_type.value, host)
    interface = router_actions.get_physical_interface(connection=ssh_connection, transceiver=transceiver, device_type=device_type)
    if interface == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return Message(message=f"Optic not present for transceiver te{transceiver}")
    return interface


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


@app.get("/ospf_cisco_xr/")
def get_ospf_cisco_xr(ospf: str):
    """Get information from Cisco XR routers for the OSPF IGP protocol."""
    # TODO rework reponses.
    ssh_connection = get_connection()
    response = router_actions.ospf_neighbor_cisco_xr(ssh_connection, ospf)
    ssh_connection.disconnect()
    if response:
        return {"status": 200, "message": "here you are you bugger"}
    else:
        return {
            "status": 404,
            "message": "No OSPF stats! IT IS BROKEN! Someone call Lucius!",
        }


@app.get("/test")
def testy_poo():
    sevone_actions.get_all_tmarcs()
    return {"message": "Test Complete"}


# @app.get("/get_config/")
# Get router config via NETCONF.
# Future feature.
# def get_config():
#     netconfig_actions.getconfig()
#     return {"status": 202, "message": "here is the config"}
