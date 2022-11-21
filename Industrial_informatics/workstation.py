import requests
'''
Inheritable class. Contains only conveyor API calls.
'''
class Conveyor: 
    def __init__(self, conveyor_api):
        self.conveyor_api = conveyor_api

    def trans_zone12(self):
        transition: tuple = (f"{self.conveyor_api}/rest/services/TransZone12", '{"destUrl" : ""}')
        r = requests.post(transition[0], data=transition[1])
        print(f'Transzone12 {r.status_code}')

    def trans_zone23(self):
        transition: tuple = (f"{self.conveyor_api}/rest/services/TransZone23", '{"destUrl" : ""}')
        r = requests.post(transition[0], data=transition[1])
        print(f'Transzone23 {r.status_code}')

    def trans_zone35(self):
        transition: tuple = (f"{self.conveyor_api}/rest/services/TransZone35", '{"destUrl" : ""}')
        r = requests.post(transition[0], data=transition[1])
        print(f'Transzone35 {r.status_code}')

    def trans_zone14(self):
        transition: tuple = (f"{self.conveyor_api}/rest/services/TransZone14", '{"destUrl" : ""}')
        r = requests.post(transition[0], data=transition[1])
        print(f'Transzone14 {r.status_code}')

    def trans_zone45(self):
        transition: tuple = (f"{self.conveyor_api}/rest/services/TransZone45", '{"destUrl" : ""}')
        r = requests.post(transition[0], data=transition[1])
        print(f'Transzone45 {r.status_code}')

    def zone1status(self):
        transition: tuple = (f"{self.conveyor_api}/rest/services/Z1", '{"destUrl" : ""}')
        r = requests.post(transition[0], data=transition[1])
        print('Zone 1 status', r.status_code, r.text["PalletID"])
        return r.content["PalletID"]

    def zone2status(self):
        transition: tuple = (f"{self.conveyor_api}/rest/services/Z2", '{"destUrl" : ""}')
        r = requests.post(transition[0], data=transition[1])
        print('Zone 2 status',r.status_code, r.text["PalletID"])
        return r.content["PalletID"]

    def zone3status(self):
        transition: tuple = (f"{self.conveyor_api}/rest/services/Z3", '{"destUrl" : ""}')
        r = requests.post(transition[0], data=transition[1])
        print('Zone 3 status',r.status_code, r.text["PalletID"])
        return r.content["PalletID"]

    def zone4status(self):
        transition: tuple = (f"{self.conveyor_api}/rest/services/Z4", '{"destUrl" : ""}')
        r = requests.post(transition[0], data=transition[1])
        print('Zone 4 status',r.status_code, r.text["PalletID"])
        return r.content["PalletID"]

    def zone5status(self):
        transition: tuple = (f"{self.conveyor_api}/rest/services/Z5", '{"destUrl" : ""}')
        r = requests.post(transition[0], data=transition[1])
        print('Zone 5 status',r.status_code, r.text["PalletID"])
        return r.content["PalletID"]


'''
Inheritable class. Contains only robot API calls.
'''
class Robot():
    def __init__(self, robot_api) -> None:
        self.robot_api = robot_api

    def draw(self):
        draw: tuple = (f"{self.robot_api}/rest/services/Draw3", '{"destUrl" : ""}')
        r = requests.post(draw[0], data=draw[1])
        print('Draw 3', r.status_code)



'''
Workstation class that contains conveyor and robot API calls and the zone states.
'''
class Workstation(Conveyor, Robot):
    #Class constructor
    def __init__(self, wsID):
        self.wsID: int = wsID
        self.robot_api: str = f"http://192.168.{wsID}.1"
        self.conveyor_api: str = f"http://192.168.{wsID}.2"
        self.zone_states: dict[str:bool] = {"Z"+str(i+1): False for i in range(5)}
        Conveyor.__init__(self, self.conveyor_api)
        Robot.__init__(self, self.robot_api)

