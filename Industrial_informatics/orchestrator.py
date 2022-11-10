import time
import requests
from workstation import Workstation

#palletID: alphanumeric
class Pallet:
    def __init__(self, palletID, assembled=False):
        self.palletID: int = palletID
        self.assembled: bool = assembled


class Orchestrator:
    def __init__(self) -> None:
        self.id = 3
        self.workstation = Workstation(self.id)
        self.workstation.zone_states["Z3"] = True
        self.__subscribe_to_events()

    def __subscribe_to_events(self):
        r1 = requests.post(f"http://192.168.{self.id}.2/rest/events/Z1_Changed/notifs", data="{“destUrl” : “http://192.168.0."+self.id*10+":8080”}")
        r2 = requests.post(f"http://192.168.{self.id}.2/rest/events/Z2_Changed/notifs", data="{“destUrl” : “http://192.168.0."+self.id*10+":8080”}")
        r3 = requests.post(f"http://192.168.{self.id}.2/rest/events/Z3_Changed/notifs", data="{“destUrl” : “http://192.168.0."+self.id*10+":8080”}")
        r4 = requests.post(f"http://192.168.{self.id}.2/rest/events/Z4_Changed/notifs", data="{“destUrl” : “http://192.168.0."+self.id*10+":8080”}")
        r5 = requests.post(f"http://192.168.{self.id}.2/rest/events/Z5_Changed/notifs", data="{“destUrl” : “http://192.168.0."+self.id*10+":8080”}")
        print(f"Zone 1 request: {r1.status_code}\nZone 2 request: {r2.status_code}\nZone 3 request: {r3.status_code}\nZone 4 request: {r4.status_code} \nZone 5 request: {r5.status_code}")


    def change_ws_state(self, zone_id:str) -> None:
        self.workstation.zone_states[zone_id] = not self.workstation.zone_states[zone_id]


    def transferPallet(self, fromWS, toWS):
        print ("Orchestrator transfering pallet started...")
        p = fromWS.removePallet()
        toWS.addPallet(p)
        print ("Orchestrator: Transfered pallet " + p.palletID + " from: " + fromWS.wsID + " to: " + toWS.wsID)


