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
        self.pallets: list[Pallet] = []
        self.__subscribe_to_events()

    def add_pallet(self):
        self.pallets.append(Pallet(len(self.pallets+1)))

    def __subscribe_to_events(self):
        r1 = requests.post(f"http://192.168.{self.id}.2/rest/events/Z1_Changed/notifs", data="{“destUrl” : “http://192.168.0."+self.id*10+":8080”}")
        r2 = requests.post(f"http://192.168.{self.id}.2/rest/events/Z2_Changed/notifs", data="{“destUrl” : “http://192.168.0."+self.id*10+":8080”}")
        r3 = requests.post(f"http://192.168.{self.id}.2/rest/events/Z3_Changed/notifs", data="{“destUrl” : “http://192.168.0."+self.id*10+":8080”}")
        r4 = requests.post(f"http://192.168.{self.id}.2/rest/events/Z4_Changed/notifs", data="{“destUrl” : “http://192.168.0."+self.id*10+":8080”}")
        r5 = requests.post(f"http://192.168.{self.id}.2/rest/events/Z5_Changed/notifs", data="{“destUrl” : “http://192.168.0."+self.id*10+":8080”}")
        r6 = requests.post(f"http://192.168.{self.id}.1/rest/events/DrawEndExecution/notifs", data="{“destUrl” : “http://192.168.0."+self.id*10+":8080”}")

        print(f"Zone 1 request: {r1.status_code}\nZone 2 request: {r2.status_code}\nZone 3 request: {r3.status_code}\nZone 4 request: {r4.status_code} \nZone 5 request: {r5.status_code}")


    def change_ws_state(self, zone_id:str) -> None:
        self.workstation.zone_states[zone_id] = not self.workstation.zone_states[zone_id]
        if self.workstation.zone_states["Z1"]:
            self.add_pallet()


    def move_pallet(self, from_zone, pallet_id) -> None:
        if from_zone == "Z1":
            if self.pallets[pallet_id].assembled or self.workstation.zone_states["Z2"]:
                self.workstation.trans_zone14()
                # TODO add hold if the zone 4 is busy..
            else:
                self.workstation.trans_zone12()

        elif from_zone == "Z2":
            if not self.workstation.zone_states["Z3"]:
                self.workstation.trans_zone23()
        
        elif from_zone == "Z3":
            if not self.workstation.zone_states["Z5"] and not self.workstation.zone_states["Z4"] :
                self.workstation.trans_zone35()
                    # TODO add hold if the zone 4 and 5 is busy..

        elif from_zone == "Z4":
            if not self.workstation.zone_states["Z5"]:
                self.workstation.trans_zone45()


    def robot_draw(self, pallet_id):
        self.workstation.draw()
        self.pallets[pallet_id].assembled = True





