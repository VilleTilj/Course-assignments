import requests

class Workstation:
    #Class constructor
    def __init__(self, wsID):
        self.wsID: int = wsID
        self.robot_api: str = "http://192.168.{ws_id}.1"
        self.conveyor_api: str = "http://192.168.{ws_id}.2"
        self.zone_states: dict[str:bool] = {"Z"+str(i+1): False for i in range(5)}


class Conveyor: 
    def __init__(ws_id):
        transzone12: tuple = (f"http://192.168.{ws_id}.2/rest/services/TransZone12", {'destUrl' : ""})


class Robot():
    def __init__(self) -> None:
        pass

