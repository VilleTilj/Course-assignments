import requests

class Workstation(Conveyor):
    #Class constructor
    def __init__(self, wsID):
        self.wsID = wsID
        self.palletList = []



class Conveyor: 
    def __init__(ws_id):
        transzone12: tuple = (f"http://192.168.{ws_id}.y/rest/services/TransZone12", {'destUrl' : ""})


class Robot():
    def __init__(self) -> None:
        pass