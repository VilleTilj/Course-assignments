import requests
from workstation import Workstation
import logging
from time import sleep

#palletID: alphanumeric
class Pallet:
    def __init__(self, palletID, assembled=False):
        self.palletID: int = palletID
        self.assembled: bool = assembled

'''
Class to subscribe to RTU events and operate workstation, in other words move the pallet in the workstation and operate robot.
'''
class Orchestrator:
    def __init__(self, ws) -> None:
        logging.basicConfig(level=logging.INFO)
        self.id = str(ws)
        self.workstation = Workstation(self.id)
        self.pallets: dict[str:Pallet] = {}
        self.__subscribe_to_events()

    def add_pallet(self, pallet_id):
        self.pallets[pallet_id] = Pallet(palletID=pallet_id)
        logging.info("New pallet added to the workstation.")

    def __subscribe_to_events(self):
        # NOTE does not work with workstations with number higher than 9.
        r1 = requests.post(f'http://192.168.{self.id}.2/rest/events/Z1_Changed/notifs', data='{"destUrl" : "http://192.168.0.'+self.id+'0:8080/events"}')
        r2 = requests.post(f'http://192.168.{self.id}.2/rest/events/Z2_Changed/notifs', data='{"destUrl" : "http://192.168.0.'+self.id+'0:8080/events"}')
        r3 = requests.post(f'http://192.168.{self.id}.2/rest/events/Z3_Changed/notifs', data='{"destUrl" : "http://192.168.0.'+self.id+'0:8080/events"}')
        r4 = requests.post(f'http://192.168.{self.id}.2/rest/events/Z4_Changed/notifs', data='{"destUrl" : "http://192.168.0.'+self.id+'0:8080/events"}')
        r5 = requests.post(f'http://192.168.{self.id}.2/rest/events/Z5_Changed/notifs', data='{"destUrl" : "http://192.168.0.'+self.id+'0:8080/events"}')
        r6 = requests.post(f'http://192.168.{self.id}.1/rest/events/DrawEndExecution/notifs', data='{"destUrl" : "http://192.168.0.'+self.id+'0:8080/events"}')

        logging.info(f"Zone 1 request: {r1.status_code}\nZone 2 request: {r2.status_code}\nZone 3 request: {r3.status_code}\nZone 4 request: {r4.status_code} \nZone 5 request: {r5.status_code}\nDraw end execution request: {r6.status_code}")


    # Keep track about the workstation zone states.
    def change_ws_state(self, zone_id:str, pallet_id:str='-1', new_pallet:bool=False) -> None:
        self.workstation.zone_states[zone_id] = not self.workstation.zone_states[zone_id]
        if new_pallet:
            self.add_pallet(pallet_id)
            

    ''' Logic to move the pllet through workstations.
        @param from_zone: zone location where pallet is moving further.
        @param pallet_id: pallets id
    '''
    def move_pallet(self, from_zone: str, pallet_id: str = '123') -> None:
        if from_zone == "Z1":
            if self.pallets.get(pallet_id).assembled or self.workstation.zone2status() != '-1':
                self.workstation.trans_zone14()
                sleep(1)
            else:
                self.workstation.trans_zone12()
                sleep(1)

        elif from_zone == "Z2":
            if self.workstation.zone3status() == '-1':
                self.workstation.trans_zone23()
                sleep(1)
                if self.workstation.zone1status() != '-1':
                    self.move_pallet('Z1', self.workstation.zone1status())

        elif from_zone == "Z5":
                # Collision avoidance
                if self.workstation.zone5status() == '-1' and self.workstation.zone4status() != '-1':
                    self.workstation.trans_zone45()
                    sleep(1)

                elif self.workstation.zone5status() == '-1' and self.workstation.zone3status() != '-1':
                    self.workstation.trans_zone35()
                    sleep(1)

                if self.workstation.zone3status() == '-1' and self.workstation.zone2status() != '-1':
                    self.workstation.trans_zone23()
        
        elif from_zone == "Z3":
            if self.workstation.zone5status() == '-1':
                self.workstation.trans_zone35()

                if self.workstation.zone2status() != '-1':
                    self.workstation.trans_zone23()

        elif from_zone == "Z4":
            if self.workstation.zone5status() == '-1':
                self.workstation.trans_zone45()
                sleep(1)

        
    # Draw "assemble" part with the robot.
    def robot_draw(self, pallet_id):
        self.workstation.draw()
        self.pallets[pallet_id].assembled = True
        logging.info("Pallet assembled")
        '''if True:

            if self.workstation.zone5status() == '-1' and self.workstation.zone4status() != '-1':
                self.workstation.trans_zone45()
                sleep(1)

            elif self.workstation.zone5status() == '-1' and self.workstation.zone3status() != '-1':
                self.workstation.trans_zone35()
                sleep(1)
            '''




