from classes.physical_interfaces import PhysicalInterface

def transciever_phy(connection, transciever) -> PhysicalInterface:
    response = connection.send_command(f"show controllers {transciever} all")

    transciever_details = PhysicalInterface()

    split_responce = response.split("\n")
    for i in split_responce:
        if ":" in i:
            i = i.replace("\t", "")
            i_list = i.split(":")
            if i_list[0] == "Replace This":
                pass
