import time

#palletID: alphanumeric
# part: cylinder, spring
class Pallet:
    def __init__(self, palletID, part):
        self.palletID = palletID
        self.part = part





class Orchestrator:
    def transferPallet(self, fromWS, toWS):
        print ("Orchestrator transfering pallet started...")
        p = fromWS.removePallet()
        toWS.addPallet(p)
        print ("Orchestrator: Transfered pallet " + p.palletID + " from: " + fromWS.wsID + " to: " + toWS.wsID)


