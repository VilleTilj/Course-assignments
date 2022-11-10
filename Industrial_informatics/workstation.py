import requests

class Conveyor: 
    def __init__(self, conveyor_api, robot_api):
        self.conveyor_api = conveyor_api

    def trans_zone12(self):
        transition: tuple = (f"{self.conveyor_api}/rest/services/TransZone12", {'destUrl' : ""})
        r = requests.post(transition[0], data=transition[1])
        print(r.status_code)

    def trans_zone23(self):
        transition: tuple = (f"{self.conveyor_api}/rest/services/TransZone23", {'destUrl' : ""})
        r = requests.post(transition[0], data=transition[1])
        print(r.status_code)

    def trans_zone35(self):
        transition: tuple = (f"{self.conveyor_api}/rest/services/TransZone35", {'destUrl' : ""})
        r = requests.post(transition[0], data=transition[1])
        print(r.status_code)

    def trans_zone14(self):
        transition: tuple = (f"{self.conveyor_api}/rest/services/TransZone14", {'destUrl' : ""})
        r = requests.post(transition[0], data=transition[1])
        print(r.status_code)

    def trans_zone45(self):
        transition: tuple = (f"{self.conveyor_api}/rest/services/TransZone45", {'destUrl' : ""})
        r = requests.post(transition[0], data=transition[1])
        print(r.status_code)



class Robot():
    def __init__(self, robot_api) -> None:
        self.robot_api = robot_api

    def draw(self):
        draw: tuple = (f"{self.robot_api}/rest/services/Draw3", {'destUrl' : ""})
        r = requests.post(draw[0], data=draw[1])
        print(r.status_code)




class Workstation(Conveyor, Robot):
    #Class constructor
    def __init__(self, wsID):
        self.wsID: int = wsID
        self.robot_api: str = "http://192.168.{ws_id}.1"
        self.conveyor_api: str = "http://192.168.{ws_id}.2"
        self.zone_states: dict[str:bool] = {"Z"+str(i+1): False for i in range(5)}
        Conveyor.__init__(self.conveyor_api)
        Robot.__init__(self.robot_api)

