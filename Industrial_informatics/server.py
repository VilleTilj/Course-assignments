from flask import Flask, request, jsonify
from orchestrator import Orchestrator

app = Flask(__name__)
orchestrator = Orchestrator()


# Method to move pallet through workstation using events
def check_zone_change(data):
    if data["id"] == "Z1_Changed" and  data["payload"]["PalletID"] != '-1':
        orchestrator.change_ws_state("Z1",pallet_id=data["payload"]["PalletID"], new_pallet=True)
        orchestrator.move_pallet("Z1", data["payload"]["PalletID"])
    elif data["id"] == "Z2_Changed" and  data["payload"]["PalletID"] != '-1':
            orchestrator.move_pallet("Z2", data["payload"]["PalletID"])
    elif data["id"] == "Z3_Changed" and  data["payload"]["PalletID"] != '-1':
            orchestrator.move_pallet("Z3", data["payload"]["PalletID"])
            pass #orchestrator.robot_draw(data["payload"]["PalletID"])
            
    elif data["id"] == "DrawEndExecution":
            orchestrator.move_pallet("Z3", data["payload"]["PalletID"])
    elif data["id"] == "Z4_Changed" and  data["payload"]["PalletID"] != '-1':
            orchestrator.move_pallet("Z4", data["payload"]["PalletID"])
    elif data["id"] == "Z5_Changed" and  data["payload"]["PalletID"] != '-1':
            orchestrator.move_pallet("Z5", data["payload"]["PalletID"])
    

'''
Alternative method to move the pallet through workstation. Does not require event subscription.

def transfer_pallet():
    # Poll until there is a pallet in zone 1.
    while True:
        if orchestrator.workstation.zone1status() != -1:
            break
        sleep(1)

    orchestrator.change_ws_state("Z1", new_pallet=True)
    if orchestrator.workstation.zone_states["Z1"]:
        orchestrator.move_pallet("Z1", 1)
   
    
    if orchestrator.workstation.zone_states["Z2"]:
        orchestrator.move_pallet("Z2", 1)
    
    if orchestrator.workstation.zone_states["Z3"]:
        orchestrator.robot_draw(1)
        sleep(15)
        orchestrator.move_pallet("Z3", 1)

    if orchestrator.workstation.zone_states["Z4"]:
        orchestrator.move_pallet("Z4", 1)

    if not orchestrator.workstation.zone_states["Z5"]:
        orchestrator.move_pallet("Z5", 1)
'''

@app.route('/events',methods=['POST'])
def receive_events():
    print("endpoint hit")
    data = request.json
    print(data)
    check_zone_change(data)
    return "ok"


if __name__ == '__main__':

    app.run(host='192.168.0.40', port=8080, debug=True)